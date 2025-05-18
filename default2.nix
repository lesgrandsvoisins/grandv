# shell.nix       
let                                                                                                      
  # We pin to a specific nixpkgs commit for reproducibility and because in our situation, it is run with user-rights.
  # pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae.tar.gz") {};
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/tags/24.11.tar.gz") {};
  packageOverrides = pkgs.callPackage ./python-packages.nix {};
  python = pkgs.python312.override {inherit packageOverrides; };
in pkgs.mkShell {
  env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.libz
    pkgs.openldap
  ];
  packages = with pkgs; [
    (python.withPackages (python-pkgs: with python-pkgs; [
      # select Python packages here
      pillow
      gunicorn
      pip
      libsass
      python-ldap
      pyscss
      django-libsass
      pylibjpeg-libjpeg
      pypdf2
      #venvShellHook
      pq
      # python3
      aiosasl
      psycopg2
      django
      wagtail
      python-dotenv
      dj-database-url 
      # psycopg2-binary
      django-taggit
      #wagtail-modeladmin
      wagtailmenus
      ## Public facing server, I think
      python-keycloak
      ## Dev
      ## djlint
      django-debug-toolbar
      ## Feature for future Testing
      ## django-meta
    ]))
  ];

  # shellHook = ''
  #   # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
  #   # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
  #   export PIP_PREFIX=$(pwd)/_build/pip_packages
  #   export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
  #   export PATH="$PIP_PREFIX/bin:$PATH"
  #   unset SOURCE_DATE_EPOCH
  # '';

}

