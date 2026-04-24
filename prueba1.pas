program validacion;
var
  suma, cont: integer;
begin
  suma := 0;
  cont := 5;
  while cont > 0 do
  begin
    suma := suma + cont;
    cont := cont - 1
  end;
  write(suma)
end.