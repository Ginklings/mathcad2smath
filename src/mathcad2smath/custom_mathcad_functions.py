#!/usr/bin/env python
# -*- coding: utf-8 -*-

sm_file_string = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<?application progid="SMath Studio Desktop" version="0.99.7822.147"?>
<worksheet xmlns="http://smath.info/schemas/worksheet/1.0">
  <settings ppi="96">
    <identity>
      <id>0f860c4b-3b6f-412b-a71d-9901d93a7e28</id>
      <revision>11</revision>
    </identity>
    <calculation>
      <precision>2</precision>
      <exponentialThreshold>5</exponentialThreshold>
      <trailingZeros>false</trailingZeros>
      <significantDigitsMode>false</significantDigitsMode>
      <roundingMode>0</roundingMode>
      <fractions>decimal</fractions>
    </calculation>
    <pageModel active="false" viewMode="2" printGrid="false" printAreas="true" simpleEqualsOnly="false" printBackgroundImages="true">
      <paper id="9" orientation="Portrait" width="827" height="1169" />
      <margins left="39" right="39" top="49" bottom="49" />
      <header alignment="Center" color="#a9a9a9">&amp;[DATE] &amp;[TIME] - &amp;[FILENAME]</header>
      <footer alignment="Center" color="#a9a9a9">&amp;[PAGENUM] / &amp;[COUNT]</footer>
      <backgrounds />
    </pageModel>
    <dependencies>
      <assembly name="SMath Studio Desktop" version="0.99.7822.147" guid="a37cba83-b69c-4c71-9992-55ff666763bd" />
      <assembly name="MathRegion" version="1.11.7822.147" guid="02f1ab51-215b-466e-a74d-5d8b1cf85e8d" />
      <assembly name="SpecialFunctions" version="1.12.7822.147" guid="2814e667-4e12-48b1-8d51-194e480eabc5" />
    </dependencies>
  </settings>
  <regions type="content">
    <region left="72" top="45" width="224" height="79" color="#000000" fontSize="10">
      <math>
        <input>
          <e type="operand">x</e>
          <e type="function" args="1">floor</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">x</e>
          <e type="operator" args="2">≤</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">1</e>
          <e type="operator" args="2">-</e>
          <e type="function" args="3">if</e>
          <e type="operator" args="2">:</e>
        </input>
      </math>
    </region>
    <region left="423" top="45" width="216" height="79" color="#000000" fontSize="10">
      <math>
        <input>
          <e type="operand">x</e>
          <e type="function" args="1">ceil</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">x</e>
          <e type="operator" args="2">≥</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">x</e>
          <e type="operand">0</e>
          <e type="function" args="2">round</e>
          <e type="operand">1</e>
          <e type="operator" args="2">+</e>
          <e type="function" args="3">if</e>
          <e type="operator" args="2">:</e>
        </input>
      </math>
    </region>
    <region left="81" top="162" width="92" height="24" color="#000000" fontSize="10">
      <math>
        <input>
          <e type="operand">Percent</e>
          <e type="operand" style="unit">%</e>
          <e type="operator" args="2">:</e>
        </input>
      </math>
    </region>
  </regions>
</worksheet>'''

def save_sm_file(basedir=''):
    custom = basedir + '//' + 'custom.sm' if basedir else 'custom.sm'
    with open(custom, 'w', encoding='utf-8') as f:
        f.write(sm_file_string)
save_sm_file()