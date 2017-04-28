import os 
from uge_cooker.cooker import Cooker

def main():
	cwd = os.path.dirname(os.path.realpath(__file__))
	cooker = Cooker(
		env=os.path.join(cwd, "env.json"),
		cwd=cwd
	)
	cooker.order(
		recipe=os.path.join(cwd, "recipe.json")
	)
	cooker.cook()

if __name__ == "__main__":
	main()
