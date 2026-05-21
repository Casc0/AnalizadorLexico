{ Programa valido: procedimientos con y sin parametros }
program procs;
var
  x: integer;
procedure imprimir(n: integer);
begin
  write(n)
end;
procedure saludar;
begin
  write(1)
end
begin
  read(x);
  imprimir(x);
  saludar
end.
