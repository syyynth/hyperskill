import docker
from hstest import StageTest, dynamic_test, CheckResult

ancestor = "hyper-web-app"

project_images = ["hyper-web-app"]

class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    # @dynamic_test()
    # def test1(self):
    #     """Tests image of container, state and exposed port"""
    #     all_containers = self.client.containers.list(all=True)
    #     for container in all_containers:
    #         if container.attrs.get("Config").get("Image") == ancestor:
    #             if not container.attrs.get("State").get("Running"):
    #                 return CheckResult.correct()
    #             else:
    #                 return CheckResult.wrong("The container shouldn't be running!")
    #
    #     return CheckResult.wrong(f"Couldn't find a container from the '{ancestor}' ancestor!")

    @dynamic_test()
    def test2(self):
        """Tests if the container is deleted"""
        all_containers = self.client.containers.list(all=True)
        for container in all_containers:
            if container.attrs.get("Config").get("Image") == ancestor:
                return CheckResult.wrong(f"You should delete the container for the ancestor '{ancestor}'!")

        return CheckResult.correct()

    @dynamic_test()
    def test3(self):
        """Tests if the image is removed from the system"""
        images_text = " ".join([str(image) for image in self.client.images.list()])
        for image in project_images:
            if image in images_text:
                return CheckResult.wrong(f"You should delete the image '{image}'!")

        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
