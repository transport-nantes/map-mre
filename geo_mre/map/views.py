from django.views.generic.base import TemplateView

import folium
from folium import plugins

class MapView(TemplateView):
    template_name = 'map/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empty_map = """{"type": "FeatureCollection", "name": "reseau_velo_metropolitain_empty", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": [{"type": "Feature", "properties": {"id": 2}, "geometry": {"type": "MultiLineString", "coordinates": []}}]}"""

        figure = folium.Figure()
        lat = 47.2184
        lon = -1.5556
        geomap = folium.Map(location=[lat, lon], zoom_start=8)
        folium.TileLayer('cartodb positron', attr="CartoDB").add_to(geomap)
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
        geomap.add_to(figure)
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
        #folium.LayerControl(hideSingleBase=True).add_to(geomap)

        map_root = geomap.get_root()
        map_root.header._children['bootstrap'] = folium.elements.JavascriptLink('https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js')
        map_root.header._children['bootstrap_css'] = folium.elements.CssLink('https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css')
        map_root.header._children['bootstrap_theme_css'] = folium.elements.CssLink('https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap-theme.min.css')

        # This is the Layer filter to enable / disable datas on map
        folium.LayerControl(hideSingleBase=True).add_to(geomap)

        root = figure.get_root()
        root.render()

        context["map"] = figure
        return context

