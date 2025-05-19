{
  description = "A flake for the correct python envrionment for this website";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {self, nixpkgs, ...}: 
  let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
    pkgName = "wagtailenv";
    packageOverrides = pkgs.callPackage ./flake-python-packages.nix {};
    python = pkgs.python312.override {inherit packageOverrides; };
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
          # wagtailmenus
          # django-meta
          ## Public facing server, I think
          python-keycloak
          ## Dev
          ## djlint
          django-debug-toolbar
          ## Feature for future Testing
          ## django-meta
        ]))
      ];
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      packages = packages;
    };
    packages.x86_64-linux.default = derivation {
      name = pkgName;
      builder = with pkgs; "${python}/bin/python";
      args = [ "-m gunicorn" "--env WAGTAIL_ENV='production'" "--access-logfile /tmp/access.log" "--error-logfile /tmp/error.log" "--chdir ${self}" "--workers 12" "--bind 0.0.0.0:8999" "settings.wsgi:application"];
      outputs = ["bin"];
      system = "x86_64-linux";
      src = ./.;
      buildInputs = [ packages ];
    };
    # packages.x86_64-linux.lib = pkgs.mkDerivation {
    #   packages = packages;
    # };
  };
}