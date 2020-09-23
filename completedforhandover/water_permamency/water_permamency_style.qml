<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" minScale="1e+08" version="3.4.11-Madeira" styleCategories="AllStyleCategories" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer type="singlebandpseudocolor" classificationMax="100" opacity="1" alphaBand="-1" classificationMin="1" band="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" classificationMode="1">
          <colorramp type="gradient" name="[source]">
            <prop v="65,215,24,255" k="color1"/>
            <prop v="43,131,186,255" k="color2"/>
            <prop v="0" k="discrete"/>
            <prop v="gradient" k="rampType"/>
            <prop v="0.5325;253,23,69,255" k="stops"/>
          </colorramp>
          <item value="1" alpha="255" color="#41d718" label="1"/>
          <item value="25.75" alpha="255" color="#9a7d2d" label="25.75"/>
          <item value="50.5" alpha="255" color="#f22343" label="50.5"/>
          <item value="75.25" alpha="255" color="#9b497c" label="75.25"/>
          <item value="100" alpha="255" color="#2b83ba" label="100"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeBlue="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100" grayscaleMode="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler zoomedInResampler="bilinear" maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
