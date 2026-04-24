{ Prueba de error 2: numero mal formado y caracter no reconocido }
program errores2;
var
  x: integer;
  y: integer;
begin
  x := 42abc;
  y := x + 7;
  y := y @ 3;
  write(y)
end.
