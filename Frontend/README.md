Jak chcecie odpalic to trzeba pobrac node.js i potem w terminalu:

$ npm create vite@latest BSIAW -- --template react

> npx
> create-vite BSIAW --template react

│
◇ Package name:
│ bsiaw
│
◇ Use rolldown-vite (Experimental)?:
│ No
│
◇ Install with npm and start now?
│ Yes

Potem to:

cd BSIAW && git init && git remote add origin https://github.com/tomek-019/Projekt_WebSec && git fetch origin && git reset --hard origin/main

i na koniec:

npm install

a potem odpalacie:
npm run dev
