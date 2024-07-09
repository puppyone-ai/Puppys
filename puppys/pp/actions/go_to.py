from puppys.pp.actions.load_env import load_env, unload_env
from puppys.pp.actions.explore import explore
from puppys.env.env import Env
from puppys.pp.main import Puppy


def go_to(puppy_instance, new_env_node):

    """
    change the env_node to another env
    """
    pre_env_node = puppy_instance.env_node
    unload_env(puppy_instance=puppy_instance, env_node=pre_env_node)
    puppy_instance.env_node = new_env_node



if __name__ == "__main__":

    def value_test(self):
        pass

    Museum = Puppy( value=value_test,name="the maple", description="It's a beautiful place")

    Museum.Louvre = Env(value="good", name="Louvre", description="It's a beautiful museum")
    Museum.Eiffel = Env(value="bad", name="Eiffel", description="It's a ugly tower")

    Museum.load_env()

    print(Museum.puppy_vars.runtime_dict)

    go_to(Museum,Museum.Louvre)

    Museum.load_env()

    print(Museum.puppy_vars.runtime_dict)
