#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x4cf819e6, "module_layout" },
	{ 0xf9418c06, "param_ops_int" },
	{ 0xfd14437d, "video_ioctl2" },
	{ 0x933cc27e, "_dev_err" },
	{ 0xfba9c57b, "device_create_file" },
	{ 0xdb714c58, "__video_register_device" },
	{ 0xd9a5ea54, "__init_waitqueue_head" },
	{ 0xc6f46339, "init_timer_key" },
	{ 0xb58f9fe7, "video_device_release" },
	{ 0xee33c8c8, "video_device_alloc" },
	{ 0x2f319651, "v4l2_device_register" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0x92540fbf, "finish_wait" },
	{ 0x8c26d495, "prepare_to_wait_event" },
	{ 0x1000e51, "schedule" },
	{ 0xfe487975, "init_wait_entry" },
	{ 0x69acdf38, "memcpy" },
	{ 0x800473f, "__cond_resched" },
	{ 0x4f00afd3, "kmem_cache_alloc_trace" },
	{ 0x696f0c3, "kmalloc_caches" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x6309f6a2, "vm_insert_page" },
	{ 0xc82c6e84, "vmalloc_to_page" },
	{ 0x13c49cc2, "_copy_from_user" },
	{ 0x88db9f48, "__check_object_size" },
	{ 0x65487097, "__x86_indirect_thunk_rax" },
	{ 0x37befc70, "jiffies_to_msecs" },
	{ 0x40a9b349, "vzalloc" },
	{ 0xd6ee688f, "vmalloc" },
	{ 0xbcab6ee6, "sscanf" },
	{ 0x5c3c7387, "kstrtoull" },
	{ 0xd4254459, "v4l2_device_unregister" },
	{ 0x26fa9659, "video_unregister_device" },
	{ 0x37a0cba, "kfree" },
	{ 0xb1b6df6f, "device_remove_file" },
	{ 0x999e8297, "vfree" },
	{ 0x5e515be6, "ktime_get_ts64" },
	{ 0xd0da656b, "__stack_chk_fail" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x656e4a6e, "snprintf" },
	{ 0xe46021ca, "_raw_spin_unlock_bh" },
	{ 0xc3690fc, "_raw_spin_lock_bh" },
	{ 0x97934ecf, "del_timer_sync" },
	{ 0xcbd4898c, "fortify_panic" },
	{ 0xdd64e639, "strscpy" },
	{ 0xa916b694, "strnlen" },
	{ 0x92997ed8, "_printk" },
	{ 0x87a21cb3, "__ubsan_handle_out_of_bounds" },
	{ 0x6ed15256, "video_devdata" },
	{ 0x33a21a09, "pv_ops" },
	{ 0x3eeb2322, "__wake_up" },
	{ 0xc38c83b8, "mod_timer" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0xbdfb6dbb, "__fentry__" },
};

MODULE_INFO(depends, "videodev");


MODULE_INFO(srcversion, "9CB4B3276778EF6860A5C15");
