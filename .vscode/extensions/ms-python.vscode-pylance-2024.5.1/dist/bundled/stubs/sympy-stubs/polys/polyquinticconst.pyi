from typing import Any
from sympy.utilities import public

x = ...
@public
class PolyQuintic:
    def __init__(self, poly) -> None:
        ...
    
    @property
    def f20(self) -> Any:
        ...
    
    @property
    def b(self) -> tuple[list[Any], list[int], list[int], list[int], list[int]]:
        ...
    
    @property
    def o(self) -> list[int]:
        ...
    
    @property
    def a(self) -> list[int]:
        ...
    
    @property
    def c(self) -> list[int]:
        ...
    
    @property
    def F(self):
        ...
    
    def l0(self, theta):
        ...
    
    def T(self, theta, d) -> list[int]:
        ...
    
    def order(self, theta, d):
        ...
    
    def uv(self, theta, d) -> tuple[Any, Any]:
        ...
    
    @property
    def zeta(self) -> list[Any]:
        ...
    


