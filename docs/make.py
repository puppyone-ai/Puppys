
from pathlib import Path
import pdoc
import shutil

here = Path(__file__).parent

if __name__ == "__main__":

    logo_path = here / "logo.png"
    
    output_directory = here / "build"

    shutil.copy(logo_path, output_directory / "logo.png")


    pdoc.render.configure(
        edit_url_map={
            "puppys": "https://github.com/PuppyAgent/Puppys/tree/main/puppys/",
        },
        logo=  "logo.png",
        logo_link="https://github.com/PuppyAgent/Puppys",
        template_directory=here / "my_template",  # 指定自定义模板目录

        # footer_text=f"puppys {puppys.__version__}",
    )

    pdoc.pdoc(
       here/ ".." / "puppys",
        output_directory= here / "build",
    )
