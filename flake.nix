{
  description = "A flake for the correct python envrionment for this website";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {self, nixpkgs, flake-utils, ...}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
        };
        pkgName = "wagtailenv";
        packageOverrides = pkgs.callPackage ./flake-python-packages.nix {};
        python = pkgs.python311.override {inherit packageOverrides; };
        # packages = with pkgs; [
        #    (python.withPackages (python-pkgs: with python-pkgs; [
        pythonEnv = python.withPackages (ps: with ps; [
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
        ]);
        src = ./.;
      in {
      packages.default = pkgs.writeShellApplication {
        name = "run-django";
        runtimeInputs = [ pythonEnv pkgs.git ];
        text = ''
          export PYTHONPATH=$PWD
          export DJANGO_SETTINGS_MODULE=settings
          echo "Starting --env WAGTAIL_ENV='production' --access-logfile /tmp/access.log --error-logfile /tmp/error.log --chdir ${self} --workers 12 --bind 0.0.0.0:8999 settings.wsgi:application --reload"
        '';
      };
      devShells.default = pkgs.mkShell {
        buildInputs = [ pythonEnv pkgs.git ];
        shellHook = ''
          export PYTHONPATH=$PWD
          export DJANGO_SETTINGS_MODULE=settings
          echo "Dev shell ready. You can run the server with: gunicorn myproject.wsgi:application --bind 127.0.0.1:8000 --reload"
        '';
      };
      # devShells.x86_64-linux.default = pkgs.mkShell {
      #   packages = packages;
      # };
    }); 
  }