
from pathlib import Path
import pdoc
import shutil

here = Path(__file__).parent

if __name__ == "__main__":

    pdoc.render.configure(
        edit_url_map={
            "puppys": "https://github.com/PuppyAgent/Puppys/tree/main/puppys/",
        },
        logo=  "/docs/logo.png",
        logo_link="https://github.com/PuppyAgent/Puppys",
        template_directory=here / "my_template", 

        # footer_text=f"puppys {puppys.__version__}",
    )

    pdoc.pdoc(
       here/ ".." / "puppys",
        output_directory= here / "build",
    )
