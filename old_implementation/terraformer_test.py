import  terraformer_class

terraformer = terraformer_class.Terraformer()
assert terraformer.coordinate == (0,0)
assert terraformer.density == 50
assert terraformer.width == 10
assert terraformer.length == 10
map_ = []
for i in range(0,terraformer.length):
            row_ = []
            for j in range(0,terraformer.width):
                row_.append(0)
            map_.append(row_)
assert terraformer.gradient_map != map_
assert terraformer.map == map_
assert terraformer.terrain_map == map_
assert terraformer.check_map == map_
terraformer.create_object()
terraformer.set_terrain(6)
print(terraformer.print_terrain())