let
  pkgs = import <nixpkgs> {};
  python = pkgs.python312;
  pythonPackages = python.pkgs;
in with pkgs; mkShell {
  packages = [
    python
    pythonPackages.venvShellHook
    gdal
    tippecanoe
  ];

  shellHook = ''
    SOURCE_DATE_EPOCH=$(date +%s)
    VENV=.venv

    if test ! -d $VENV; then
      python3 -m venv $VENV
    fi
    source ./$VENV/bin/activate
    export PYTHONPATH=`pwd`/$VENV/${python.sitePackages}/:$PYTHONPATH
    pip install -e .
  '';

  postShellHook = ''
    ln -sf ${python.sitePackages}/* ./.venv/lib/python3.12/site-packages
  '';
}
