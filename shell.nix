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

			terrafom
			terraform-ls
	];

	shellHook = ''
		echo "Environment up !"
		exec zsh
		'';
}
