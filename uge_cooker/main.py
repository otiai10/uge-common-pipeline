from cooker import Cooker


def cooker_main():
	print("This is uge_cooker cli")
	cooker = Cooker("./example_project/env.json")
	cooker.introduce()
