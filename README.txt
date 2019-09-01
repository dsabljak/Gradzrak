Da bi se mogao pokretati kod koji je u ovom projektu treba se definirati PYTHONPATH varijabla okruženja.
Slijedite korake ovsino o operacijskom sustavu kojeg koristite.

## LINUX(UBUNTU) ##

1. Otvorite terminal(shortcut : ctrl+alt+t)
2. Pozicionirajte se u home direktorij
        cd ~
3. Otvorite s nekim editorom file .bashrc (ovdje se otvara sa sublime text editorom, al može bilo što)
        subl ./.bashrc
4. Na dnu file-a dodati

        # Python path variable
        export PYTHONPATH="${path_to_project}"

    Recimo ako se projekt nalazi /home/project/Gradzrak onda je path_to_project jednak /home/project


## WINDOWS ##

1. Upišite u tražilicu enviromental variable(varijable okruženja)
2. Tamo napravite vrijablu koje se zove PYTHONPATH i postavite da ima vrijednost ${path_to_project}
    Recimo ako se projekt nalazi C:/home/project/Gradzrak onda je path_to_project jednak C:/home/project



I to bi trebalo biti to sad bi se sve trebalo pokretati bez problema, naravno uz to da imate sve ostale
potrebne module kao recimo shapely.
Ukoliko nemate sve module onda koristite python-ov pip modul za instalaciju modula.