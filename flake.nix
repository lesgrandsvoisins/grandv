{
  description = "A flake for the correct python envrionment for this website";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {self, nixpkgs, ...}: let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
    packageOverrides = pkgs.callPackage ./python-packages.nix {};
    python = pkgs.python312.override {inherit packageOverrides; };
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
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
          wagtail-modeladmin
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
    };
  };
}