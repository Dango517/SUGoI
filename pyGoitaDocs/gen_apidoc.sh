cd source
sphinx-apidoc -f -o . ../../pyGoita
cd ../../
sphinx-build -b html pyGoitaDocs/source/ pyGoitaDocs/build/html
