{ Programa valido: if/else anidados, while con cuerpo compuesto, expresiones logicas }
program anidados;
var
  a, b, c: integer;
  flag: boolean;
begin
  read(a);
  read(b);
  c := 0;
  flag := false;
  if a > 0 then
    if b > 0 then
      c := a + b
    else
      c := a - b
  else
    c := 0 - a;
  while c > 0 do
  begin
    c := c - 1;
    if c = 5 then
      flag := true
  end;
  if flag and (c <= 0) then
    write(c)
  else
    write(0)
end.
