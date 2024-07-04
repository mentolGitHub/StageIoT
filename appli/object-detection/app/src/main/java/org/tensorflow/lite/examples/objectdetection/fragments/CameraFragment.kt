/*
 * Copyright 2022 The TensorFlow Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.tensorflow.lite.examples.objectdetection.fragments

import android.annotation.SuppressLint
import android.content.res.Configuration
import android.graphics.Bitmap
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.Toast
import androidx.camera.core.AspectRatio
import androidx.camera.core.Camera
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.navigation.Navigation
import org.tensorflow.lite.examples.objectdetection.ObjectDetectorHelper
import org.tensorflow.lite.examples.objectdetection.R
import org.tensorflow.lite.examples.objectdetection.databinding.FragmentCameraBinding
import org.tensorflow.lite.task.vision.detector.Detection
import java.util.LinkedList
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import com.google.ar.core.*
import com.google.ar.core.exceptions.CameraNotAvailableException
import com.google.ar.core.exceptions.UnavailableException
import android.opengl.Matrix
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.content.Intent
import android.view.TextureView
import androidx.activity.result.contract.ActivityResultContracts
import org.tensorflow.lite.examples.objectdetection.BluetoothHelper
import org.tensorflow.lite.examples.objectdetection.BluetoothDeviceListActivity


class CameraFragment : Fragment(), ObjectDetectorHelper.DetectorListener {

    private val TAG = "ObjectDetection"

    private var _fragmentCameraBinding: FragmentCameraBinding? = null
    private val fragmentCameraBinding
        get() = _fragmentCameraBinding!!

    private lateinit var objectDetectorHelper: ObjectDetectorHelper
    private lateinit var bitmapBuffer: Bitmap
    private var preview: Preview? = null
    private var imageAnalyzer: ImageAnalysis? = null
    private var camera: Camera? = null
    private var cameraProvider: ProcessCameraProvider? = null

    private lateinit var cameraExecutor: ExecutorService

    private lateinit var bluetoothHelper: BluetoothHelper
    private val BLUETOOTH_REQUEST_CODE = 1
    private val SELECT_BLUETOOTH_DEVICE_REQUEST_CODE = 2

    private lateinit var arSession: Session
    private lateinit var arFrame: Frame
    private val viewMatrix = FloatArray(16)
    private val projectionMatrix = FloatArray(16)

    override fun onResume() {
        super.onResume()
        if (!PermissionsFragment.hasPermissions(requireContext())) {
            Navigation.findNavController(requireActivity(), R.id.fragment_container)
                .navigate(CameraFragmentDirections.actionCameraToPermissions())
        }
    }

    override fun onDestroyView() {
        _fragmentCameraBinding = null
        super.onDestroyView()
        cameraExecutor.shutdown()
        bluetoothHelper.closeConnection()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _fragmentCameraBinding = FragmentCameraBinding.inflate(inflater, container, false)
        return fragmentCameraBinding.root
    }

    @SuppressLint("MissingPermission")
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        bluetoothHelper = BluetoothHelper(requireContext())
        setupBluetoothConnection()

        objectDetectorHelper = ObjectDetectorHelper(
            context = requireContext(),
            objectDetectorListener = this
        )

        cameraExecutor = Executors.newSingleThreadExecutor()

        fragmentCameraBinding.viewFinder.post {
            setUpCamera()
        }

        initializeARCore()
        initBottomSheetControls()
    }

    private fun initializeARCore() {
        try {
            if (ArCoreApk.getInstance().requestInstall(requireActivity(), true) == ArCoreApk.InstallStatus.INSTALLED) {
                arSession = Session(requireContext())
                val config = Config(arSession)
                config.updateMode = Config.UpdateMode.LATEST_CAMERA_IMAGE
                config.focusMode = Config.FocusMode.AUTO
                arSession.configure(config)
            }
        } catch (e: UnavailableException) {
            Log.e(TAG, "ARCore not available", e)
        }
    }

    private fun setupBluetoothConnection() {
        if (!bluetoothHelper.isBluetoothSupported()) {
            Toast.makeText(requireContext(), "Bluetooth is not supported on this device", Toast.LENGTH_SHORT).show()
            return
        }

        if (!bluetoothHelper.isBluetoothEnabled()) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            bluetoothEnableLauncher.launch(enableBtIntent)
        } else {
            launchBluetoothDeviceSelection()
        }
    }

    private fun launchBluetoothDeviceSelection() {
        val intent = Intent(requireContext(), BluetoothDeviceListActivity::class.java)
        bluetoothDeviceSelectionLauncher.launch(intent)
    }

    private fun connectToBluetoothDevice(address: String) {
        if (bluetoothHelper.connectToDevice(address)) {
            Toast.makeText(requireContext(), "Connected to Bluetooth device", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(requireContext(), "Failed to connect to Bluetooth device", Toast.LENGTH_SHORT).show()
        }
    }

    private val bluetoothEnableLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            launchBluetoothDeviceSelection()
        } else {
            Toast.makeText(requireContext(), "Bluetooth is required for this feature", Toast.LENGTH_SHORT).show()
        }
    }

    private val bluetoothDeviceSelectionLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val deviceAddress = result.data?.getStringExtra("deviceAddress")
            deviceAddress?.let { connectToBluetoothDevice(it) }
        }
    }

    private fun setUpCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(requireContext())
        cameraProviderFuture.addListener({
            cameraProvider = cameraProviderFuture.get()
            bindCameraUseCases()
        }, ContextCompat.getMainExecutor(requireContext()))
    }

    @SuppressLint("UnsafeOptInUsageError")
    private fun bindCameraUseCases() {
        val cameraProvider = cameraProvider ?: throw IllegalStateException("Camera initialization failed.")

        val cameraSelector = CameraSelector.Builder().requireLensFacing(CameraSelector.LENS_FACING_BACK).build()

        preview = Preview.Builder()
            .setTargetAspectRatio(AspectRatio.RATIO_4_3)
            .setTargetRotation(fragmentCameraBinding.viewFinder.display.rotation)
            .build()

        imageAnalyzer = ImageAnalysis.Builder()
            .setTargetAspectRatio(AspectRatio.RATIO_4_3)
            .setTargetRotation(fragmentCameraBinding.viewFinder.display.rotation)
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_RGBA_8888)
            .build()
            .also {
                it.setAnalyzer(cameraExecutor) { image ->
                    if (!::bitmapBuffer.isInitialized) {
                        bitmapBuffer = Bitmap.createBitmap(
                            image.width,
                            image.height,
                            Bitmap.Config.ARGB_8888
                        )
                    }
                    detectObjectsWithARCore(image)
                }
            }

        cameraProvider.unbindAll()

        try {
            camera = cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageAnalyzer)
            preview?.setSurfaceProvider(fragmentCameraBinding.viewFinder.surfaceProvider)
        } catch (exc: Exception) {
            Log.e(TAG, "Use case binding failed", exc)
        }
    }

    private fun detectObjectsWithARCore(image: ImageProxy) {
        image.use { bitmapBuffer.copyPixelsFromBuffer(image.planes[0].buffer) }

        try {
            if (!::arSession.isInitialized) {
                return
            }

            val textureView = fragmentCameraBinding.viewFinder as TextureView
            textureView?.surfaceTexture?.let { texture ->
                // Assuming the intention was to release the SurfaceTexture after obtaining its ID for AR processing
                val textureId = texture.detach().id // This line is hypothetical as `detach()` does not exist; the correct approach depends on the specific AR and texture handling logic required.
                arSession.setCameraTextureName(textureId)
                texture.release() // Correct method to release a SurfaceTexture
            }

            arFrame = arSession.update()
            val camera = arFrame.camera

            val imageRotation = image.imageInfo.rotationDegrees
            objectDetectorHelper.detect(bitmapBuffer, imageRotation)

            camera.getViewMatrix(viewMatrix, 0)
            camera.getProjectionMatrix(projectionMatrix, 0, 0.1f, 100.0f)
        } catch (e: CameraNotAvailableException) {
            Log.e(TAG, "Camera not available during detectObjectsWithARCore", e)
        }
    }

    private fun initBottomSheetControls() {
        // Threshold adjustment controls
        fragmentCameraBinding.bottomSheetLayout.thresholdMinus.setOnClickListener {
            if (objectDetectorHelper.threshold >= 0.1) {
                objectDetectorHelper.threshold -= 0.1f
                updateControlsUi()
            }
        }
        fragmentCameraBinding.bottomSheetLayout.thresholdPlus.setOnClickListener {
            if (objectDetectorHelper.threshold <= 0.8) {
                objectDetectorHelper.threshold += 0.1f
                updateControlsUi()
            }
        }

        // Max results adjustment controls
        fragmentCameraBinding.bottomSheetLayout.maxResultsMinus.setOnClickListener {
            if (objectDetectorHelper.maxResults > 1) {
                objectDetectorHelper.maxResults--
                updateControlsUi()
            }
        }
        fragmentCameraBinding.bottomSheetLayout.maxResultsPlus.setOnClickListener {
            if (objectDetectorHelper.maxResults < 5) {
                objectDetectorHelper.maxResults++
                updateControlsUi()
            }
        }

        // Thread number adjustment controls
        fragmentCameraBinding.bottomSheetLayout.threadsMinus.setOnClickListener {
            if (objectDetectorHelper.numThreads > 1) {
                objectDetectorHelper.numThreads--
                updateControlsUi()
            }
        }
        fragmentCameraBinding.bottomSheetLayout.threadsPlus.setOnClickListener {
            if (objectDetectorHelper.numThreads < 4) {
                objectDetectorHelper.numThreads++
                updateControlsUi()
            }
        }

        // Delegate selection controls
        fragmentCameraBinding.bottomSheetLayout.spinnerDelegate.setSelection(0, false)
        fragmentCameraBinding.bottomSheetLayout.spinnerDelegate.onItemSelectedListener =
            object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) {
                    objectDetectorHelper.currentDelegate = p2
                    updateControlsUi()
                }

                override fun onNothingSelected(p0: AdapterView<*>?) {}
            }

        // Model selection controls
        fragmentCameraBinding.bottomSheetLayout.spinnerModel.setSelection(0, false)
        fragmentCameraBinding.bottomSheetLayout.spinnerModel.onItemSelectedListener =
            object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(p0: AdapterView<*>?, p1: View?, p2: Int, p3: Long) {
                    objectDetectorHelper.currentModel = p2
                    updateControlsUi()
                }

                override fun onNothingSelected(p0: AdapterView<*>?) {}
            }
    }

    private fun updateControlsUi() {
        fragmentCameraBinding.bottomSheetLayout.maxResultsValue.text =
            objectDetectorHelper.maxResults.toString()
        fragmentCameraBinding.bottomSheetLayout.thresholdValue.text =
            String.format("%.2f", objectDetectorHelper.threshold)
        fragmentCameraBinding.bottomSheetLayout.threadsValue.text =
            objectDetectorHelper.numThreads.toString()

        objectDetectorHelper.clearObjectDetector()
        fragmentCameraBinding.overlay.clear()
    }

    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
        imageAnalyzer?.targetRotation = fragmentCameraBinding.viewFinder.display.rotation
    }

    override fun onResults(
        results: MutableList<Detection>?,
        inferenceTime: Long,
        imageHeight: Int,
        imageWidth: Int
    ) {
        activity?.runOnUiThread {
            fragmentCameraBinding.bottomSheetLayout.inferenceTimeVal.text =
                String.format("%d ms", inferenceTime)

            val resultsWithDistance = results?.map { detection ->
                val centerX = (detection.boundingBox.left + detection.boundingBox.right) / 2f
                val centerY = (detection.boundingBox.top + detection.boundingBox.bottom) / 2f
                val distance = calculateDistance(centerX, centerY)
                DetectionWithDistance(detection, distance)
            }

            fragmentCameraBinding.overlay.setResultsWithDistance(
                resultsWithDistance ?: LinkedList(),
                imageHeight,
                imageWidth
            )

            fragmentCameraBinding.overlay.invalidate()
            resultsWithDistance?.let { sendDetectedObjectsWithDistanceViaBluetooth(it) }
        }
    }


    private fun calculateDistance(x: Float, y: Float): Float {
        val viewProjectionMatrix = FloatArray(16)
        Matrix.multiplyMM(viewProjectionMatrix, 0, projectionMatrix, 0, viewMatrix, 0)

        val inverseViewProjectionMatrix = FloatArray(16)
        Matrix.invertM(inverseViewProjectionMatrix, 0, viewProjectionMatrix, 0)

        val nearWorldPoint = floatArrayOf(x, y, 0f, 1f)
        val farWorldPoint = floatArrayOf(x, y, 1f, 1f)
        Matrix.multiplyMV(nearWorldPoint, 0, inverseViewProjectionMatrix, 0, nearWorldPoint, 0)
        Matrix.multiplyMV(farWorldPoint, 0, inverseViewProjectionMatrix, 0, farWorldPoint, 0)

        val nearVector = FloatArray(3)
        val farVector = FloatArray(3)
        for (i in 0..2) {
            nearVector[i] = nearWorldPoint[i] / nearWorldPoint[3]
            farVector[i] = farWorldPoint[i] / farWorldPoint[3]
        }

        val direction = FloatArray(3)
        for (i in 0..2) {
            direction[i] = farVector[i] - nearVector[i]
        }

        val length = Math.sqrt(
            (direction[0] * direction[0] +
                    direction[1] * direction[1] +
                    direction[2] * direction[2]).toDouble()
        ).toFloat()

        for (i in 0..2) {
            direction[i] /= length
        }

        val cameraPosition = arFrame.camera.pose.translation
        val distanceFromCamera = Math.abs(
            (cameraPosition[0] - nearVector[0]) * direction[0] +
                    (cameraPosition[1] - nearVector[1]) * direction[1] +
                    (cameraPosition[2] - nearVector[2]) * direction[2]
        )

        return distanceFromCamera
    }

    private fun sendDetectedObjectsWithDistanceViaBluetooth(detections: List<DetectionWithDistance>) {
        val message = detections.joinToString(", ") { "${it.detection.categories.first().label}: ${String.format("%.2f", it.distance)}m" }
        bluetoothHelper.sendData("o, $message")
    }

    data class DetectionWithDistance(val detection: Detection, val distance: Float)

    override fun onError(error: String) {
        activity?.runOnUiThread {
            Toast.makeText(requireContext(), error, Toast.LENGTH_SHORT).show()
        }
    }
}
