set number=1
set uno=1
forfiles /M *.png /C "cmd /c echo %number%&&rename "@fname .png" sus%number%.png&&set number=%number%+%uno%"
echo done!