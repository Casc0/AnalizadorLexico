{ Programa valido: funciones con y sin parametros }
program funciones;
var
  x, y: integer;
function suma(a, b: integer): integer;
begin
  suma := a + b
end;
function uno: integer;
begin
  uno := 1
end
begin
  read(x);
  read(y);
  write(suma(x, y));
  write(uno)
end.
