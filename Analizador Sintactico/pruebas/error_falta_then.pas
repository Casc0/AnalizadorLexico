{ Error sintactico: falta 'then' en la sentencia if }
program err;
var
  a: integer;
begin
  read(a);
  if a > 0
    a := 1
end.
