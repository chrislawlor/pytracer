from dataclasses import dataclass

from .color import Color
from .light import PointLight
from .primitives import Point, Vector3

DEFAULT_COLOR = Color.from_hex("FF0066")
BLACK = Color(0, 0, 0)


@dataclass(slots=True)
class Material:
    color: Color
    ambient: float
    diffuse: float
    specular: float
    shininess: float

    @classmethod
    def default(cls):
        return cls(
            color=DEFAULT_COLOR, ambient=0.1, diffuse=0.9, specular=0.9, shininess=50
        )

    def lighting(
        self,
        light: PointLight,
        position: Point,
        eye_vector: Vector3,
        normal_vector: Vector3,
    ) -> Color:
        # combine surface color with light intensity
        effective_color = self.color * light.intensity

        # find the direction to the light source
        lightv = (light.position - position).normalize()

        # calculate the ambient contribution
        ambient = effective_color * self.ambient

        # represents the cos of the angle between the
        # normal vector and the light vector. Negative
        # value means the light is on the other side
        # of the surface
        light_dot_normal = lightv.dot(normal_vector)

        if light_dot_normal < 0:
            diffuse = BLACK
            specular = BLACK
        else:
            # Calculate the diffuse contribution
            diffuse = effective_color * self.diffuse * light_dot_normal

            # reflect_dot_eye represents the cos of the angle between
            # reflection vector and the eye vector. A negative
            # value means the light is reflected away from the eye
            reflectv = -lightv.reflect(normal_vector)
            reflect_dot_eye = reflectv.dot(eye_vector)

            if reflect_dot_eye <= 0:
                specular = BLACK
            else:
                # calculate the specular contribution
                factor: float = reflect_dot_eye**self.shininess
                specular = light.intensity * self.specular * factor
        return ambient + diffuse + specular
