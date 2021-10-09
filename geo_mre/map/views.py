from django.views.generic.base import TemplateView

import folium
from folium import plugins

# Create your views here.
class MapView(TemplateView):
    template_name = 'map/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empty_map = """{"type": "FeatureCollection", "name": "reseau_velo_metropolitain_empty", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": [{"type": "Feature", "properties": {"id": 2}, "geometry": {"type": "MultiLineString", "coordinates": []}}]}"""

        lat = 47.2184
        lon = -1.5556
        geomap = folium.Map(location=[lat, lon], zoom_start=8)
        # CartoDB is a Black and white map to highlight colors
        folium.TileLayer('cartodb positron', attr="CartoDB").add_to(geomap)
        # CyclOSM displays cyclist oriented information like parking, pathways.
        folium.TileLayer(
            tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
            attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name="CyclOSM").add_to(geomap)

        # styles args : https://leafletjs.com/reference-1.6.0.html#path-option
        styles=[{'color': '#000000', "dashArray": "1 10"},
                {'color': '#9BBF85', 'weight': 7}, #006164, #9BBF85
                {'color': '#B3589A', 'weight': 7},]#B3589A , #DB4325


        geojson = empty_map
        layer_name = "i-am-a-layer-name"

        group = folium.FeatureGroup(layer_name)
        geomap.add_child(group)
        # The lambda function is mandatory to use the style_function
        # argument. It passes a dict as argument which contains datas
        # about the layer (like the coordinates).
        #
        # This dict is stored in the "_" argument, deleting it would
        # result in the first argument being overridden by the dict.
        # The variable styles is a list of dict containing args to set
        # various styles settings such as thickness, opacity, color,
        # etc.
        folium.GeoJson(geojson, name=layer_name,
                       style_function=lambda _, ind=0, style=styles: style[ind]).add_to(group)

        # This is the Layer filter to enable / disable datas on map
        folium.LayerControl(hideSingleBase=True).add_to(geomap)

        # Produce html code to embed on our page
        root = geomap.get_root()
        html = root.render()
        # Hack to prevent Boostrap 3.2 to load, causes style conflict.
        # PR is on the way to update folium as of 29/06/21
        # Deleting the extra bootstrap import solves style conflict.
        old_bs_link = "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"
        html = html.replace(old_bs_link, "")
        context["html_map"] = html

        return context

