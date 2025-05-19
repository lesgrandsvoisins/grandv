{
  description = "A flake for the correct python envrionment for this website";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # mach-nix.url = "github:DavHau/mach-nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {self, nixpkgs, flake-utils}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
        };
        pkgName = "wagtailenv";
        packageOverrides = pkgs.callPackage ./flake-python-packages.nix {};
        python = pkgs.python311.override {inherit packageOverrides; };
        # pythonPackages = python.withPackages (ps: with ps; [
        # pythonPackages = mach-nix.lib.${system}.mkPython {
        #   requirements = ''
        #   pillow
        #   gunicorn
        #   pip
        #   libsass
        #   python-ldap
        #   pyscss
        #   django-libsass
        #   pylibjpeg-libjpeg
        #   pypdf2
        #   pq
        #   aiosasl
        #   psycopg2
        #   django
        #   wagtail
        #   python-dotenv
        #   dj-database-url 
        #   # psycopg2-binary
        #   django-taggit
        #   # wagtail-modeladmin
        #   # wagtailmenus
        #   # django-meta
        #   ## Public facing server, I think
        #   python-keycloak
        #   ## Dev
        #   ## djlint
        #   django-debug-toolbar
        #   ## Feature for future Testing
        #   ## django-meta
        #   '';
        # };
        pythonPackages = python.withPackages (ps: with ps; [
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
        runtimeInputs = [ pythonPackages ];
        # runtimeInputs = [ pythonEnv pkgs.git ];
        text = ''
          export PYTHONPATH=$PWD
          export DJANGO_SETTINGS_MODULE=settings.settings
          echo "Starting gunicorn --env WAGTAIL_ENV='production' --access-logfile grandv-access.log --error-logfile grandv-error.log --workers 12 --bind 0.0.0.0:8909 settings.wsgi:application --reload"
          gunicorn --env WAGTAIL_ENV='production' --access-logfile grandv-access.log --error-logfile grandv-error.log --workers 12 --bind 0.0.0.0:8909 --reload settings.wsgi:application
        '';
      };
      devShells.default = pkgs.mkShell {
        # buildInputs = [ pythonEnv pkgs.git ];
        buildInputs = [ pythonPackages pkgs.git ];
        shellHook = ''
          export PYTHONPATH=$PWD
          export DJANGO_SETTINGS_MODULE=settings.settings
          echo "Dev shell ready. You can run the server with: gunicorn myproject.wsgi:application --bind 127.0.0.1:8909 --reload"

        '';
      };
      # devShells.x86_64-linux.default = pkgs.mkShell {
      #   packages = packages;
      # };
    }); 
  }