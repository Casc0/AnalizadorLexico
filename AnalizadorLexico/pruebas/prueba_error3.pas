{ Prueba de error 1: comentario sin cerrar }
program errores1;
var
  contador: integer;
  activo: boolean;
begin
  contador := 10;
  activo := true;
  { Este comentario nunca se cierra porque le falta la llave de cierre
  while activo do
    contador := contador - 1;
  write(contador)
end.
