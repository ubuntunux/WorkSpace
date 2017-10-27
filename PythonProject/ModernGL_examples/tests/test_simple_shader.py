import unittest

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_vertex_shader(self):
        src = '''
            #version 330
            in vec4 vertex;
            void main() {
                gl_Position = vertex;
            }
        '''

        shader = self.ctx.vertex_shader(src)
        self.assertEqual(shader.source, src)
        self.assertEqual(shader.typename, 'vertex_shader')

    def test_fragment_shader(self):
        src = '''
            #version 330
            out vec4 color;
            void main() {
                color = vec4(0.0, 0.0, 0.0, 1.0);
            }
        '''

        shader = self.ctx.fragment_shader(src)
        self.assertEqual(shader.source, src)
        self.assertEqual(shader.typename, 'fragment_shader')

    def test_geometry_shader(self):
        src = '''
            #version 330
            layout(points) in;
            layout(points, max_vertices = 1) out;
            out vec4 color;
            void main() {
                gl_Position = gl_in[0].gl_Position;
                EmitVertex();
                EndPrimitive();
            }
        '''

        shader = self.ctx.geometry_shader(src)
        self.assertEqual(shader.source, src)
        self.assertEqual(shader.typename, 'geometry_shader')

    def test_tess_control_shader(self):
        if self.ctx.version_code < 400:
            self.skipTest('OpenGL 4.0 is not supported')

        src = '''
            #version 400
            layout(vertices = 3) out;
            in vec3 vPosition[];
            out vec3 tcPosition[];
            uniform float TessLevelInner;
            uniform float TessLevelOuter;
            void main() {
                tcPosition[gl_InvocationID] = vPosition[gl_InvocationID];
                if (gl_InvocationID == 0) {
                    gl_TessLevelInner[0] = TessLevelInner;
                    gl_TessLevelOuter[0] = TessLevelOuter;
                    gl_TessLevelOuter[1] = TessLevelOuter;
                    gl_TessLevelOuter[2] = TessLevelOuter;
                }
            }
        '''

        shader = self.ctx.tess_control_shader(src)
        self.assertEqual(shader.source, src)
        self.assertEqual(shader.typename, 'tess_control_shader')

    def test_tess_evaluation_shader(self):
        if self.ctx.version_code < 400:
            self.skipTest('OpenGL 4.0 is not supported')

        src = '''
            #version 400
            layout(triangles, equal_spacing, cw) in;
            in vec3 tcPosition[];
            out vec3 tePosition;
            out vec3 tePatchDistance;
            uniform mat4 Projection;
            uniform mat4 Modelview;
            void main() {
                vec3 p0 = gl_TessCoord.x * tcPosition[0];
                vec3 p1 = gl_TessCoord.y * tcPosition[1];
                vec3 p2 = gl_TessCoord.z * tcPosition[2];
                tePatchDistance = gl_TessCoord;
                tePosition = normalize(p0 + p1 + p2);
                gl_Position = Projection * Modelview * vec4(tePosition, 1);
            }
        '''

        shader = self.ctx.tess_evaluation_shader(src)
        self.assertEqual(shader.source, src)
        self.assertEqual(shader.typename, 'tess_evaluation_shader')


if __name__ == '__main__':
    unittest.main()
