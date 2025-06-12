
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    pkgs.ffmpeg
    pkgs.ffmpeg-full
    pkgs.which
    pkgs.curl
    pkgs.wget
  ];
  
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.ffmpeg
    ];
    PYTHONBIN = "${pkgs.python311}/bin/python3.11";
    LANG = "en_US.UTF-8";
    STDERREDIRECT = "${pkgs.bash}/bin/bash";
    REPLIT_POETRY_PYPI_REPOSITORY_URL = "https://package-proxy.replit.com/pypi/";
    MPLBACKEND = "TkAgg";
    POETRY_CACHE_DIR = "${pkgs.python311}";
  };
}
