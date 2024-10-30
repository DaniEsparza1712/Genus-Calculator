# -*- coding: utf-8 -*-
"""

@author: Daniel Esparza

The MIT License
Copyright © 2024 Carlos Daniel Esparza Osuna

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
# with help from chatGPT and Enrique Rosales
import numpy as np
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.half_edge = None


class Face:
    def __init__(self):
        self.half_edge = None


class HalfEdge:
    def __init__(self):
        self.origin = None
        self.twin = None
        self.face = None
        self.next = None
        self.prev = None


def get_face_vertices(face):
    vertices = []
    start_half_edge = face.half_edge
    current_half_edge = start_half_edge
    while True:
        vertices.append(current_half_edge.vertex)
        current_half_edge = current_half_edge.next
        if current_half_edge == start_half_edge:
            break
    return vertices


def visualize_mesh(vertices, faces, vertex_color='r', edge_color='k'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot vertices
    vertices_array = np.array(vertices)
    ax.scatter(vertices_array[:, 0], vertices_array[:, 2], vertices_array[:, 1], c=vertex_color, depthshade=False)

    # Plot edges
    for face in faces:
        face_vertices = [vertices[i] for i in face]
        face_vertices.append(vertices[face[0]])  # Close the loop
        face_vertices = np.array(face_vertices)
        ax.plot(face_vertices[:, 0], face_vertices[:, 2], face_vertices[:, 1], c=edge_color)

        # Set equal aspect ratio
    ax.set_box_aspect([np.ptp(vertices_array[:, 0]), np.ptp(vertices_array[:, 0]), np.ptp(vertices_array[:, 1])])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def create_half_edge_structure(vertices, faces):
    # Create vertices
    vertex_map = {}
    for i, (x, y, z) in enumerate(vertices):
        vertex = Vertex(x, y, z)
        vertex_map[i] = vertex

    # Create half edges
    half_edges = []
    start_end_map = {}

    # Fills half_edges and start_end_map
    for face in faces:
        vertex_count = len(face)
        for i in range(vertex_count):
            start_vertex = face[i]
            end_vertex = face[(i + 1) % vertex_count]
            he = HalfEdge()
            half_edges.append(he)
            start_end_map[(start_vertex, end_vertex)] = he

    # Create faces
    face_map = {}
    for i, _ in enumerate(faces):
        face = Face()
        face_map[i] = face

    # Connect half edges to vertices
    for face_index, face_vertices in enumerate(faces):
        for i, vertex_index in enumerate(face_vertices):
            half_edge = half_edges[face_index * 3 + i]
            half_edge.origin = vertex_map[vertex_index]
            vertex_map[vertex_index].half_edge = half_edge

    # Connect half edges to faces
    for face_index, face_vertices in enumerate(faces):
        face = face_map[face_index]
        face_half_edges = [half_edges[face_index * 3 + i] for i in range(3)]
        face.half_edge = face_half_edges[0]
        for i in range(3):
            face_half_edges[i].face = face
            face_half_edges[i].next = face_half_edges[(i + 1) % 3]
            face_half_edges[i].prev = face_half_edges[(i + 2) % 3]

    # With help from Miguel Herrera
    # Connect half edges to twins
    for (start, end), he in start_end_map.items():
        if (end, start) in start_end_map:
            he.twin = start_end_map[(end, start)]
            start_end_map[(end, start)].twin = he

    return vertex_map, half_edges, face_map


# With help from ChatGPT
def find_connected_components(h_edges):
    visited = set()
    components = []

    def dfs(h_edge, dfs_component):
        stack = [h_edge]
        while stack:
            he = stack.pop()
            if he not in visited:
                visited.add(he)
                dfs_component.append(he)
                if he.twin and he.twin not in visited:
                    stack.append(he.twin)
                if he.next and he.next not in visited:
                    stack.append(he.next)
                if he.prev and he.prev not in visited:
                    stack.append(he.prev)

    for he in h_edges:
        if he not in visited:
            component = []
            dfs(he, component)
            components.append(component)

    return components


def get_euler_characteristic(component):
    vertex_set = set()
    face_set = set()
    edge_set = set()

    for he in component:
        vertex_set.add(he.origin)
        face_set.add(he.face)
        if (he.next.origin, he.origin) not in edge_set:
            edge_set.add((he.origin, he.next.origin))

    v = len(vertex_set)
    f = len(face_set)
    e = len(edge_set)

    euler_characteristic = v - e + f
    return euler_characteristic


def get_genus(euler_characteristic):
    return 1 - (euler_characteristic / 2)


def read_obj_file(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):
                vertex = list(map(float, line.strip().split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face_info = list(map(str, line.strip().split()[1:]))
                face = []
                for v in face_info:
                    vertex = v.split("/", 1)[0]
                    face.append(int(vertex))
                face = [index - 1 for index in face]
                faces.append(face)
    return vertices, faces


def show_file(file):
    # Read file
    vertices, faces = read_obj_file(file)

    # Visualize mesh
    visualize_mesh(vertices, faces)

def process_file(file):
    # Read file
    vertices, faces = read_obj_file(file)

    # convert to half-edges
    vertex_map, half_edges, face_map = create_half_edge_structure(vertices, faces)

    # Get connected components
    connected_components = find_connected_components(half_edges)

    # Add genus of each component
    genus = 0

    for component in connected_components:
        ec = get_euler_characteristic(component)
        g = get_genus(ec)
        genus += g

    return genus
