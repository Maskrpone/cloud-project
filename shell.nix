{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	buildInputs = with pkgs; [
		(python3.withPackages(ps: with ps; [
													python-lsp-server
													streamlit
													plotly
													sqlalchemy
													pip
													flake8
													pytest
		]))

			pyright
			ruff

			yamlfmt
			yaml-language-server

			dockerfile-language-server
			docker-compose-language-service

			terraform-ls
			terraform
	];

	shellHook = ''
		echo "Environment up !"
		if [ -f .env ]; then
      set -a
      source .env
      set +a
    fi
		exec zsh
		'';
}
