from avocado import Test
from avocado.utils.podman import Podman


class PodmanTest(Test):
    async def test_python_version(self):
        """
        :avocado: dependency={"type": "package", "name": "podman", "action": "check"}
        :avocado: tags=slow
        """
        podman = Podman()
        result = await podman.get_python_version("fedora:34")
        self.assertEqual(result, (3, 9, "/usr/bin/python3"))

    async def test_container_info(self):
        """
        :avocado: dependency={"type": "package", "name": "podman", "action": "check"}
        :avocado: tags=slow
        """
        podman = Podman()
        _, stdout, _ = await podman.execute("create", "fedora:34", "/bin/bash")
        container_id = stdout.decode().strip()
        result = await podman.get_container_info(container_id)
        self.assertEqual(result["Id"], container_id)

        await podman.execute("rm", container_id)

        result = await podman.get_container_info(container_id)
        self.assertEqual(result, {})
