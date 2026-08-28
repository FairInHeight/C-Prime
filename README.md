# <img src="cprime.png" width="32" height="32" style="vertical-align: -30px;" alt="icon"> C Prime

A new programming language designed to improve upon C and add modern features without creating an unmanageable amount of bloat.

# Planned feature list:

## Classes

"Class scope"
class, final, event

## Polymorphism

generic (_Generic still exists)
Ad Hoc
```c
generic add(int a, int b)
generic add(float a, float b)
```

is
Subtype
```c
class Animal
{
    void speak();
}

class Dog is Animal
{
    void speak()
    {
        bark();
    }
}  
```

ptype
Parametric
```c
ptype<T> T do_something(T a, T b)
ptype<T,U> T do_something(U a, U b)
```

## Modern Utilities
