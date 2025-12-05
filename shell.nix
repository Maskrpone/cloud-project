{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	buildInputs = with pkgs; [
		(python3.withPackages(ps: with ps; [
													python-lsp-server
													streamlit
													plotly
		]))
			# pytest
			pyright
			ruff
			docker-language-server
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
