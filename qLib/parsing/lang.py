'''
u32 xorshift(u32 x){
  x = x xor x << 13
  x = x xor x << 17
  x = x xor x << 5
  return x
}
f32 PHI = 1.618
f32 PHI2 = 1.3247
struct QRNG{
  f32 x = 0.0
  f32 next(Rand self){
    self.x = self.x + 1/PHI mod 1
    return self.x
  }
}
struct QRNG_2{
  f32 x = 0.0
  f32 y = 0.0
  QRNG_2 next(Rand self){
    self.x = self.x + 1/PHI2 mod 1
    self.y = self.y + 1/PHI2^2 mod 1
    return {self.x, self.y}
  }
}
main(){
  if a == b{
    u32 x = 5+2 mod 3 mod 2
  }
  if a == b{

  }
  else{

  }
  switch sign(a-b) // TODO: switch is poorly defined
    -1{

    }
    0{

    }
    1{

    }
  for(u32 i = 0) i < N{

  }
  for(u32 x) A{

  }
  for i < N{

  }
}
struct Vec3{ // packed?
  f32 x
  f32 y
  f32 z
  f32 dot(Vec3 self, Vec3 other){
    return self.x other.x + self.y other.y + self.z other.z
  }
}
enum Token{
  Int
  Float
}
union Object{
  Cube
  Sphere
}
'''

from enum import Enum

class TokenType(Enum):
  Bracket = 0
  BracketEnd = 1
  SquareBracket = 2
  SquareBracketEnd = 3
  CurlyBracket = 4
  CurlyBracketEnd = 5
  Number = 6
  Symbol = 7
  Name = 8
