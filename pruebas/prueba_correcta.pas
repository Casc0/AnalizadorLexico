{ Programa correcto: calcula el maximo entre dos enteros y verifica condiciones }
program maximos;
var
  a: integer;
  b: integer;
  maximo: integer;
  sonIguales: boolean;
begin
  read(a);
  read(b);
  sonIguales := false;
  if a > b then
    maximo := a
  else
    maximo := b;
  if a = b then
    sonIguales := true;
  { Verificamos tambien con operadores adicionales }
  if a <> b then
    maximo := maximo + 0;
  if maximo >= 100 then
    maximo := maximo - 1;
  while maximo > 0 do
    maximo := maximo - 1;
  write(maximo);
  write(sonIguales)
end.
