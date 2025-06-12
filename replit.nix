
{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.ffmpeg
    pkgs.replitPackages.prybar-python311
    pkgs.replitPackages.stderred
  ];
}
