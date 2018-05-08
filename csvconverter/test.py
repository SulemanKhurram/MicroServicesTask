from flask import Flask, jsonify
from flask_restful import Resource, Api
import pika
import pandas as pd
import xml.etree.ElementTree as ET
import io
import re

body = '<ComposedBlock ID="Page1_Block15" HEIGHT="575" WIDTH="963" VPOS="768" HPOS="123" TYPE="table" xmlns="http://www.loc.gov/standards/alto/ns-v2#"><TextBlock ID="Page1_Block16" HEIGHT="53" WIDTH="46" VPOS="768" HPOS="123" language="de"><TextLine HEIGHT="14" WIDTH="32" VPOS="778" HPOS="130"><String WC="0.6299999952" CONTENT="Pos" HEIGHT="14" WIDTH="32" VPOS="778" HPOS="130" /></TextLine></TextBlock><TextBlock ID="Page1_Block17" HEIGHT="53" WIDTH="164" VPOS="768" HPOS="169" language="de"><TextLine HEIGHT="19" WIDTH="58" VPOS="777" HPOS="220"><String WC="0.7080000043" CONTENT="Menge" HEIGHT="19" WIDTH="58" VPOS="777" HPOS="220" /></TextLine></TextBlock><TextBlock ID="Page1_Block18" HEIGHT="53" WIDTH="448" VPOS="768" HPOS="333" language="de"><TextLine HEIGHT="15" WIDTH="37" VPOS="777" HPOS="343"><String WC="0.8025000095" CONTENT="Text" HEIGHT="15" WIDTH="37" VPOS="777" HPOS="343" /></TextLine></TextBlock><TextBlock ID="Page1_Block19" HEIGHT="53" WIDTH="136" VPOS="768" HPOS="781" language="de"><TextLine HEIGHT="18" WIDTH="92" VPOS="777" HPOS="801"><String WC="0.8799999952" CONTENT="Einzelpreis" HEIGHT="18" WIDTH="92" VPOS="777" HPOS="801" /></TextLine></TextBlock><TextBlock ID="Page1_Block20" HEIGHT="53" WIDTH="169" VPOS="768" HPOS="917" language="de"><TextLine HEIGHT="18" WIDTH="110" VPOS="777" HPOS="943"><String WC="0.9027272463" CONTENT="Gesamtpreis" HEIGHT="18" WIDTH="110" VPOS="777" HPOS="943" /></TextLine></TextBlock><TextBlock ID="Page1_Block21" HEIGHT="29" WIDTH="448" VPOS="821" HPOS="333" language="de"><TextLine HEIGHT="14" WIDTH="304" VPOS="828" HPOS="343"><String WC="0.6416666508" CONTENT="Lieferschein" HEIGHT="14" WIDTH="93" VPOS="828" HPOS="343" /><SP WIDTH="4" VPOS="828" HPOS="437" /><String WC="0.6999999881" CONTENT="Nr." HEIGHT="14" WIDTH="21" VPOS="828" HPOS="442" /><SP WIDTH="4" VPOS="829" HPOS="464" /><String WC="0.4779999852" CONTENT="44968" HEIGHT="13" WIDTH="48" VPOS="829" HPOS="469" /><SP WIDTH="4" VPOS="829" HPOS="518" /><String WC="0.3199999928" CONTENT="vom" HEIGHT="11" WIDTH="32" VPOS="831" HPOS="523" /><SP WIDTH="4" VPOS="829" HPOS="556" /><String WC="0.7799999714" CONTENT="05.12.2016" HEIGHT="14" WIDTH="86" VPOS="828" HPOS="561" /></TextLine></TextBlock><TextBlock ID="Page1_Block22" HEIGHT="28" WIDTH="46" VPOS="850" HPOS="123" language="de"><TextLine HEIGHT="14" WIDTH="6" VPOS="856" HPOS="136"><String WC="0.75" CONTENT="1" HEIGHT="14" WIDTH="6" VPOS="856" HPOS="136" /></TextLine></TextBlock><TextBlock ID="Page1_Block23" HEIGHT="28" WIDTH="82" VPOS="850" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="33" VPOS="856" HPOS="211"><String WC="0.6800000072" CONTENT="1,00" HEIGHT="15" WIDTH="33" VPOS="856" HPOS="211" /></TextLine></TextBlock><TextBlock ID="Page1_Block24" HEIGHT="28" WIDTH="448" VPOS="850" HPOS="333" language="de"><TextLine HEIGHT="18" WIDTH="203" VPOS="855" HPOS="343"><String WC="0.7038461566" CONTENT="Blumengesteck" HEIGHT="16" WIDTH="119" VPOS="856" HPOS="343" /><SP WIDTH="3" VPOS="856" HPOS="463" /><String WC="0.6000000238" CONTENT="-" HEIGHT="2" WIDTH="5" VPOS="863" HPOS="467" /><SP WIDTH="4" VPOS="855" HPOS="473" /><String WC="0.7900000215" CONTENT="Empfang" HEIGHT="18" WIDTH="68" VPOS="855" HPOS="478" /></TextLine></TextBlock><TextBlock ID="Page1_Block25" HEIGHT="28" WIDTH="136" VPOS="850" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="57" VPOS="855" HPOS="852"><String WC="0.621999979" CONTENT="40,00" HEIGHT="15" WIDTH="43" VPOS="855" HPOS="852" /><SP WIDTH="3" VPOS="855" HPOS="896" /><String WC="0.2700000107" CONTENT="" HEIGHT="14" WIDTH="9" VPOS="855" HPOS="900" /></TextLine></TextBlock><TextBlock ID="Page1_Block26" HEIGHT="28" WIDTH="169" VPOS="850" HPOS="917" language="de"><TextLine HEIGHT="15" WIDTH="59" VPOS="855" HPOS="1017"><String WC="0.7440000176" CONTENT="40,00" HEIGHT="15" WIDTH="44" VPOS="855" HPOS="1017" /><SP WIDTH="4" VPOS="855" HPOS="1062" /><String WC="0.4600000083" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="9" VPOS="855" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block27" HEIGHT="27" WIDTH="46" VPOS="878" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="9" VPOS="884" HPOS="135"><String WC="1" CONTENT="2" HEIGHT="13" WIDTH="9" VPOS="884" HPOS="135" /></TextLine></TextBlock><TextBlock ID="Page1_Block28" HEIGHT="27" WIDTH="82" VPOS="878" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="32" VPOS="884" HPOS="212"><String WC="0.5350000262" CONTENT="1,00" HEIGHT="15" WIDTH="32" VPOS="884" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block29" HEIGHT="27" WIDTH="448" VPOS="878" HPOS="333" language="de"><TextLine HEIGHT="17" WIDTH="181" VPOS="883" HPOS="343"><String WC="0.6423076987" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="119" VPOS="883" HPOS="343" /><SP WIDTH="8" VPOS="883" HPOS="463" /><String WC="0.8000000119" CONTENT="(7.0G)" HEIGHT="17" WIDTH="52" VPOS="883" HPOS="472" /></TextLine></TextBlock><TextBlock ID="Page1_Block30" HEIGHT="27" WIDTH="136" VPOS="878" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="58" VPOS="883" HPOS="852"><String WC="0.5360000134" CONTENT="30,00" HEIGHT="15" WIDTH="43" VPOS="883" HPOS="852" /><SP WIDTH="3" VPOS="883" HPOS="896" /><String WC="0.2700000107" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="883" HPOS="900" /></TextLine></TextBlock><TextBlock ID="Page1_Block31" HEIGHT="27" WIDTH="169" VPOS="878" HPOS="917" language="de"><TextLine HEIGHT="15" WIDTH="58" VPOS="883" HPOS="1018"><String WC="0.523999989" CONTENT="30,00" HEIGHT="15" WIDTH="43" VPOS="883" HPOS="1018" /><SP WIDTH="4" VPOS="883" HPOS="1062" /><String WC="0.9900000095" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="9" VPOS="883" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block32" HEIGHT="81" WIDTH="46" VPOS="905" HPOS="123" language="de"><TextLine HEIGHT="14" WIDTH="9" VPOS="911" HPOS="135"><String WC="1" CONTENT="3" HEIGHT="14" WIDTH="9" VPOS="911" HPOS="135" /></TextLine></TextBlock><TextBlock ID="Page1_Block33" HEIGHT="81" WIDTH="82" VPOS="905" HPOS="169" language="de"><TextLine HEIGHT="16" WIDTH="32" VPOS="911" HPOS="212"><String WC="0.5575000048" CONTENT="1,00" HEIGHT="16" WIDTH="32" VPOS="911" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block34" HEIGHT="81" WIDTH="448" VPOS="905" HPOS="333" language="de"><TextLine HEIGHT="14" WIDTH="205" VPOS="910" HPOS="344"><String WC="0.9416666627" CONTENT="Blten" HEIGHT="14" WIDTH="47" VPOS="910" HPOS="344" /><SP WIDTH="4" VPOS="910" HPOS="392" /><String WC="0.7966666818" CONTENT="fr" HEIGHT="14" WIDTH="20" VPOS="910" HPOS="397" /><SP WIDTH="3" VPOS="910" HPOS="418" /><String WC="0.8933333158" CONTENT="den" HEIGHT="14" WIDTH="28" VPOS="910" HPOS="422" /><SP WIDTH="4" VPOS="910" HPOS="451" /><String WC="0.7099999785" CONTENT="WC" HEIGHT="14" WIDTH="29" VPOS="910" HPOS="456" /><SP WIDTH="4" VPOS="910" HPOS="486" /><String WC="0.5428571701" CONTENT="Bereich" HEIGHT="14" WIDTH="58" VPOS="910" HPOS="491" /></TextLine><TextLine HEIGHT="16" WIDTH="426" VPOS="937" HPOS="343"><String WC="0.6636363864" CONTENT="Gesamtsumme" HEIGHT="15" WIDTH="117" VPOS="937" HPOS="343" /><SP WIDTH="4" VPOS="938" HPOS="461" /><String WC="0.7733333111" CONTENT="des" HEIGHT="14" WIDTH="28" VPOS="938" HPOS="466" /><SP WIDTH="4" VPOS="938" HPOS="495" /><String WC="0.7416666746" CONTENT="Lieferschein" HEIGHT="15" WIDTH="93" VPOS="937" HPOS="500" /><SP WIDTH="4" VPOS="937" HPOS="594" /><String WC="0.3566666543" CONTENT="Nr." HEIGHT="14" WIDTH="21" VPOS="937" HPOS="599" /><SP WIDTH="4" VPOS="938" HPOS="621" /><String WC="0.9033333063" CONTENT="44968:" HEIGHT="14" WIDTH="52" VPOS="937" HPOS="626" /><SP WIDTH="5" VPOS="937" HPOS="679" /><String WC="0.4740000069" CONTENT="85,00" HEIGHT="16" WIDTH="43" VPOS="937" HPOS="685" /><SP WIDTH="4" VPOS="937" HPOS="729" /><String WC="1" CONTENT="EUR" HEIGHT="14" WIDTH="35" VPOS="937" HPOS="734" /></TextLine><TextLine HEIGHT="14" WIDTH="304" VPOS="965" HPOS="344"><String WC="0.6366666555" CONTENT="Lieferschein" HEIGHT="14" WIDTH="92" VPOS="965" HPOS="344" /><SP WIDTH="5" VPOS="965" HPOS="437" /><String WC="0.7166666389" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="965" HPOS="443" /><SP WIDTH="3" VPOS="965" HPOS="465" /><String WC="0.4219999909" CONTENT="44995" HEIGHT="14" WIDTH="49" VPOS="965" HPOS="469" /><SP WIDTH="3" VPOS="965" HPOS="519" /><String WC="0.349999994" CONTENT="vom" HEIGHT="11" WIDTH="33" VPOS="968" HPOS="523" /><SP WIDTH="4" VPOS="965" HPOS="557" /><String WC="0.6869999766" CONTENT="12.12.2016" HEIGHT="13" WIDTH="86" VPOS="965" HPOS="562" /></TextLine></TextBlock><TextBlock ID="Page1_Block35" HEIGHT="81" WIDTH="136" VPOS="905" HPOS="781" language="de"><TextLine HEIGHT="16" WIDTH="56" VPOS="910" HPOS="854"><String WC="0.5339999795" CONTENT="15,00" HEIGHT="16" WIDTH="41" VPOS="910" HPOS="854" /><SP WIDTH="3" VPOS="910" HPOS="896" /><String WC="0.2599999905" CONTENT="" HEIGHT="13" WIDTH="10" VPOS="910" HPOS="900" /></TextLine></TextBlock><TextBlock ID="Page1_Block36" HEIGHT="81" WIDTH="169" VPOS="905" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="57" VPOS="910" HPOS="1019"><String WC="0.8140000105" CONTENT="15,00" HEIGHT="15" WIDTH="43" VPOS="911" HPOS="1019" /><SP WIDTH="3" VPOS="910" HPOS="1063" /><String WC="0.3000000119" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="9" VPOS="910" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block37" HEIGHT="29" WIDTH="46" VPOS="986" HPOS="123" language="de"><TextLine HEIGHT="12" WIDTH="5" VPOS="994" HPOS="137"><String WC="0.6899999976" CONTENT="1" HEIGHT="12" WIDTH="5" VPOS="994" HPOS="137" /></TextLine></TextBlock><TextBlock ID="Page1_Block38" HEIGHT="29" WIDTH="82" VPOS="986" HPOS="169" language="de"><TextLine HEIGHT="16" WIDTH="33" VPOS="993" HPOS="212"><String WC="0.8199999928" CONTENT="1,00" HEIGHT="16" WIDTH="33" VPOS="993" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block39" HEIGHT="29" WIDTH="448" VPOS="986" HPOS="333" language="de"><TextLine HEIGHT="17" WIDTH="203" VPOS="993" HPOS="344"><String WC="0.6215384603" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="118" VPOS="993" HPOS="344" /><SP WIDTH="3" VPOS="993" HPOS="463" /><String WC="0.5699999928" CONTENT="-" HEIGHT="2" WIDTH="5" VPOS="1000" HPOS="467" /><SP WIDTH="4" VPOS="993" HPOS="473" /><String WC="0.6657142639" CONTENT="Empfang" HEIGHT="16" WIDTH="69" VPOS="993" HPOS="478" /></TextLine></TextBlock><TextBlock ID="Page1_Block40" HEIGHT="29" WIDTH="136" VPOS="986" HPOS="781" language="de"><TextLine HEIGHT="16" WIDTH="58" VPOS="992" HPOS="853"><String WC="0.6700000167" CONTENT="40,00" HEIGHT="16" WIDTH="43" VPOS="992" HPOS="853" /><SP WIDTH="3" VPOS="992" HPOS="897" /><String WC="0.3600000143" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="992" HPOS="901" /></TextLine></TextBlock><TextBlock ID="Page1_Block41" HEIGHT="29" WIDTH="169" VPOS="986" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="59" VPOS="992" HPOS="1018"><String WC="0.8640000224" CONTENT="40,00" HEIGHT="16" WIDTH="44" VPOS="992" HPOS="1018" /><SP WIDTH="3" VPOS="992" HPOS="1063" /><String WC="0.5799999833" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="992" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block42" HEIGHT="27" WIDTH="46" VPOS="1015" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="9" VPOS="1021" HPOS="135"><String WC="1" CONTENT="2" HEIGHT="13" WIDTH="9" VPOS="1021" HPOS="135" /></TextLine></TextBlock><TextBlock ID="Page1_Block43" HEIGHT="27" WIDTH="82" VPOS="1015" HPOS="169" language="de"><TextLine HEIGHT="16" WIDTH="33" VPOS="1020" HPOS="212"><String WC="0.5475000143" CONTENT="1,00" HEIGHT="16" WIDTH="33" VPOS="1020" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block44" HEIGHT="27" WIDTH="448" VPOS="1015" HPOS="333" language="de"><TextLine HEIGHT="17" WIDTH="180" VPOS="1020" HPOS="344"><String WC="0.7099999785" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="118" VPOS="1020" HPOS="344" /><SP WIDTH="9" VPOS="1020" HPOS="463" /><String WC="0.7883333564" CONTENT="(7.0G)" HEIGHT="16" WIDTH="51" VPOS="1020" HPOS="473" /></TextLine></TextBlock><TextBlock ID="Page1_Block45" HEIGHT="27" WIDTH="136" VPOS="1015" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="58" VPOS="1020" HPOS="853"><String WC="0.6399999857" CONTENT="30,00" HEIGHT="15" WIDTH="42" VPOS="1020" HPOS="853" /><SP WIDTH="4" VPOS="1020" HPOS="896" /><String WC="0.4900000095" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1020" HPOS="901" /></TextLine></TextBlock><TextBlock ID="Page1_Block46" HEIGHT="27" WIDTH="169" VPOS="1015" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="58" VPOS="1019" HPOS="1018"><String WC="0.6460000277" CONTENT="30,00" HEIGHT="16" WIDTH="44" VPOS="1019" HPOS="1018" /><SP WIDTH="3" VPOS="1019" HPOS="1063" /><String WC="0.2099999934" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="9" VPOS="1019" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block47" HEIGHT="81" WIDTH="46" VPOS="1042" HPOS="123" language="de"><TextLine HEIGHT="14" WIDTH="10" VPOS="1048" HPOS="135"><String WC="0.8000000119" CONTENT="3" HEIGHT="14" WIDTH="10" VPOS="1048" HPOS="135" /></TextLine></TextBlock><TextBlock ID="Page1_Block48" HEIGHT="81" WIDTH="82" VPOS="1042" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="33" VPOS="1048" HPOS="212"><String WC="0.3975000083" CONTENT="1,00" HEIGHT="15" WIDTH="33" VPOS="1048" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block49" HEIGHT="81" WIDTH="448" VPOS="1042" HPOS="333" language="de"><TextLine HEIGHT="15" WIDTH="205" VPOS="1047" HPOS="344"><String WC="0.6733333468" CONTENT="Bl\xc3\xbcten" HEIGHT="14" WIDTH="48" VPOS="1048" HPOS="344" /><SP WIDTH="3" VPOS="1048" HPOS="393" /><String WC="0.896666646" CONTENT="fr" HEIGHT="13" WIDTH="21" VPOS="1048" HPOS="397" /><SP WIDTH="3" VPOS="1048" HPOS="419" /><String WC="0.426666677" CONTENT="den" HEIGHT="14" WIDTH="28" VPOS="1048" HPOS="423" /><SP WIDTH="4" VPOS="1048" HPOS="452" /><String WC="1" CONTENT="WC" HEIGHT="14" WIDTH="28" VPOS="1047" HPOS="457" /><SP WIDTH="5" VPOS="1047" HPOS="486" /><String WC="0.7314285636" CONTENT="Bereich" HEIGHT="13" WIDTH="57" VPOS="1048" HPOS="492" /></TextLine><TextLine HEIGHT="15" WIDTH="425" VPOS="1075" HPOS="344"><String WC="0.6218181849" CONTENT="Gesamtsumme" HEIGHT="14" WIDTH="117" VPOS="1075" HPOS="344" /><SP WIDTH="4" VPOS="1075" HPOS="462" /><String WC="0.7233333588" CONTENT="des" HEIGHT="13" WIDTH="27" VPOS="1075" HPOS="467" /><SP WIDTH="4" VPOS="1075" HPOS="495" /><String WC="0.7416666746" CONTENT="Lieferschein" HEIGHT="13" WIDTH="93" VPOS="1075" HPOS="500" /><SP WIDTH="5" VPOS="1075" HPOS="594" /><String WC="0.7333333492" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="1075" HPOS="600" /><SP WIDTH="4" VPOS="1075" HPOS="622" /><String WC="0.7966666818" CONTENT="44995:" HEIGHT="13" WIDTH="52" VPOS="1075" HPOS="627" /><SP WIDTH="4" VPOS="1075" HPOS="680" /><String WC="0.6019999981" CONTENT="85,00" HEIGHT="15" WIDTH="43" VPOS="1075" HPOS="685" /><SP WIDTH="5" VPOS="1075" HPOS="729" /><String WC="1" CONTENT="EUR" HEIGHT="13" WIDTH="34" VPOS="1075" HPOS="735" /></TextLine><TextLine HEIGHT="14" WIDTH="304" VPOS="1102" HPOS="344"><String WC="0.8616666794" CONTENT="Lieferschein" HEIGHT="14" WIDTH="93" VPOS="1102" HPOS="344" /><SP WIDTH="4" VPOS="1102" HPOS="438" /><String WC="0.6966666579" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="1102" HPOS="443" /><SP WIDTH="4" VPOS="1103" HPOS="465" /><String WC="0.8700000048" CONTENT="45022" HEIGHT="14" WIDTH="48" VPOS="1102" HPOS="470" /><SP WIDTH="4" VPOS="1102" HPOS="519" /><String WC="0.6133333445" CONTENT="vom" HEIGHT="9" WIDTH="32" VPOS="1106" HPOS="524" /><SP WIDTH="5" VPOS="1102" HPOS="557" /><String WC="0.8600000143" CONTENT="19.12.2016" HEIGHT="13" WIDTH="85" VPOS="1102" HPOS="563" /></TextLine></TextBlock><TextBlock ID="Page1_Block50" HEIGHT="81" WIDTH="136" VPOS="1042" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="56" VPOS="1047" HPOS="855"><String WC="0.8299999833" CONTENT="15,00" HEIGHT="14" WIDTH="41" VPOS="1048" HPOS="855" /><SP WIDTH="3" VPOS="1047" HPOS="897" /><String WC="0.4600000083" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="1047" HPOS="901" /></TextLine></TextBlock><TextBlock ID="Page1_Block51" HEIGHT="81" WIDTH="169" VPOS="1042" HPOS="917" language="de"><TextLine HEIGHT="15" WIDTH="57" VPOS="1047" HPOS="1020"><String WC="0.4679999948" CONTENT="15,00" HEIGHT="15" WIDTH="42" VPOS="1047" HPOS="1020" /><SP WIDTH="3" VPOS="1047" HPOS="1063" /><String WC="0.2899999917" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1047" HPOS="1067" /></TextLine></TextBlock><TextBlock ID="Page1_Block52" HEIGHT="29" WIDTH="46" VPOS="1123" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="6" VPOS="1130" HPOS="137"><String WC="1" CONTENT="1" HEIGHT="13" WIDTH="6" VPOS="1130" HPOS="137" /></TextLine></TextBlock><TextBlock ID="Page1_Block53" HEIGHT="29" WIDTH="82" VPOS="1123" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="33" VPOS="1130" HPOS="212"><String WC="0.5425000191" CONTENT="1,00" HEIGHT="15" WIDTH="33" VPOS="1130" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block54" HEIGHT="29" WIDTH="448" VPOS="1123" HPOS="333" language="de"><TextLine HEIGHT="17" WIDTH="203" VPOS="1129" HPOS="345"><String WC="0.7923076749" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="118" VPOS="1129" HPOS="345" /><SP WIDTH="3" VPOS="1129" HPOS="464" /><String WC="0.5500000119" CONTENT="-" HEIGHT="3" WIDTH="5" VPOS="1136" HPOS="468" /><SP WIDTH="4" VPOS="1129" HPOS="474" /><String WC="0.8057143092" CONTENT="Empfang" HEIGHT="17" WIDTH="69" VPOS="1129" HPOS="479" /></TextLine></TextBlock><TextBlock ID="Page1_Block55" HEIGHT="29" WIDTH="136" VPOS="1123" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="58" VPOS="1129" HPOS="853"><String WC="0.6420000196" CONTENT="40.00" HEIGHT="15" WIDTH="43" VPOS="1129" HPOS="853" /><SP WIDTH="3" VPOS="1129" HPOS="897" /><String WC="0.3600000143" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="1129" HPOS="901" /></TextLine></TextBlock><TextBlock ID="Page1_Block56" HEIGHT="29" WIDTH="169" VPOS="1123" HPOS="917" language="de"><TextLine HEIGHT="15" WIDTH="59" VPOS="1129" HPOS="1018"><String WC="0.6159999967" CONTENT="40,00" HEIGHT="15" WIDTH="44" VPOS="1129" HPOS="1018" /><SP WIDTH="4" VPOS="1129" HPOS="1063" /><String WC="0.4499999881" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="9" VPOS="1129" HPOS="1068" /></TextLine></TextBlock><TextBlock ID="Page1_Block57" HEIGHT="27" WIDTH="46" VPOS="1152" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="9" VPOS="1158" HPOS="136"><String WC="1" CONTENT="2" HEIGHT="13" WIDTH="9" VPOS="1158" HPOS="136" /></TextLine></TextBlock><TextBlock ID="Page1_Block58" HEIGHT="27" WIDTH="82" VPOS="1152" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="33" VPOS="1158" HPOS="212"><String WC="0.5099999905" CONTENT="1,00" HEIGHT="15" WIDTH="33" VPOS="1158" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block59" HEIGHT="27" WIDTH="448" VPOS="1152" HPOS="333" language="de"><TextLine HEIGHT="17" WIDTH="180" VPOS="1157" HPOS="345"><String WC="0.8100000024" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="118" VPOS="1157" HPOS="345" /><SP WIDTH="8" VPOS="1157" HPOS="464" /><String WC="0.6583333611" CONTENT="(7.0G)" HEIGHT="17" WIDTH="52" VPOS="1157" HPOS="473" /></TextLine></TextBlock><TextBlock ID="Page1_Block60" HEIGHT="27" WIDTH="136" VPOS="1152" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="57" VPOS="1157" HPOS="854"><String WC="0.4399999976" CONTENT="30,00" HEIGHT="15" WIDTH="42" VPOS="1157" HPOS="854" /><SP WIDTH="3" VPOS="1157" HPOS="897" /><String WC="0.3300000131" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1157" HPOS="901" /></TextLine></TextBlock><TextBlock ID="Page1_Block61" HEIGHT="27" WIDTH="169" VPOS="1152" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="59" VPOS="1156" HPOS="1019"><String WC="0.5180000067" CONTENT="30,00" HEIGHT="15" WIDTH="43" VPOS="1157" HPOS="1019" /><SP WIDTH="4" VPOS="1156" HPOS="1063" /><String WC="0.2399999946" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="1156" HPOS="1068" /></TextLine></TextBlock><TextBlock ID="Page1_Block62" HEIGHT="81" WIDTH="46" VPOS="1179" HPOS="123" language="de"><TextLine HEIGHT="14" WIDTH="9" VPOS="1185" HPOS="136"><String WC="1" CONTENT="3" HEIGHT="14" WIDTH="9" VPOS="1185" HPOS="136" /></TextLine></TextBlock><TextBlock ID="Page1_Block63" HEIGHT="81" WIDTH="82" VPOS="1179" HPOS="169" language="de"><TextLine HEIGHT="17" WIDTH="33" VPOS="1184" HPOS="212"><String WC="0.3449999988" CONTENT="1,00" HEIGHT="17" WIDTH="33" VPOS="1184" HPOS="212" /></TextLine></TextBlock><TextBlock ID="Page1_Block64" HEIGHT="81" WIDTH="448" VPOS="1179" HPOS="333" language="de"><TextLine HEIGHT="14" WIDTH="205" VPOS="1184" HPOS="345"><String WC="0.6316666603" CONTENT="Bl\xc3\xbcten" HEIGHT="14" WIDTH="48" VPOS="1184" HPOS="345" /><SP WIDTH="3" VPOS="1184" HPOS="394" /><String WC="1" CONTENT="f\xc3\xbcr" HEIGHT="14" WIDTH="21" VPOS="1184" HPOS="398" /><SP WIDTH="3" VPOS="1184" HPOS="420" /><String WC="0.6266666651" CONTENT="den" HEIGHT="14" WIDTH="28" VPOS="1184" HPOS="424" /><SP WIDTH="3" VPOS="1184" HPOS="453" /><String WC="0.8450000286" CONTENT="WC" HEIGHT="14" WIDTH="29" VPOS="1184" HPOS="457" /><SP WIDTH="5" VPOS="1184" HPOS="487" /><String WC="0.6942856908" CONTENT="Bereich" HEIGHT="14" WIDTH="57" VPOS="1184" HPOS="493" /></TextLine><TextLine HEIGHT="15" WIDTH="425" VPOS="1212" HPOS="345"><String WC="0.521818161" CONTENT="Gesamtsumme" HEIGHT="14" WIDTH="117" VPOS="1212" HPOS="345" /><SP WIDTH="3" VPOS="1212" HPOS="463" /><String WC="0.8366666436" CONTENT="des" HEIGHT="13" WIDTH="28" VPOS="1212" HPOS="467" /><SP WIDTH="4" VPOS="1212" HPOS="496" /><String WC="0.7225000262" CONTENT="Lieferschein" HEIGHT="13" WIDTH="93" VPOS="1212" HPOS="501" /><SP WIDTH="5" VPOS="1212" HPOS="595" /><String WC="0.5600000024" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="1212" HPOS="601" /><SP WIDTH="3" VPOS="1212" HPOS="623" /><String WC="0.8299999833" CONTENT="45022:" HEIGHT="13" WIDTH="52" VPOS="1212" HPOS="627" /><SP WIDTH="6" VPOS="1212" HPOS="680" /><String WC="0.5799999833" CONTENT="85,00" HEIGHT="15" WIDTH="42" VPOS="1212" HPOS="687" /><SP WIDTH="4" VPOS="1212" HPOS="730" /><String WC="1" CONTENT="EUR" HEIGHT="13" WIDTH="35" VPOS="1212" HPOS="735" /></TextLine><TextLine HEIGHT="14" WIDTH="304" VPOS="1239" HPOS="345"><String WC="0.7649999857" CONTENT="Lieferschein" HEIGHT="14" WIDTH="92" VPOS="1239" HPOS="345" /><SP WIDTH="5" VPOS="1239" HPOS="438" /><String WC="0.5266666412" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="1239" HPOS="444" /><SP WIDTH="4" VPOS="1240" HPOS="466" /><String WC="0.6560000181" CONTENT="45034" HEIGHT="14" WIDTH="48" VPOS="1239" HPOS="471" /><SP WIDTH="4" VPOS="1239" HPOS="520" /><String WC="0.1366666704" CONTENT="vom" HEIGHT="10" WIDTH="32" VPOS="1242" HPOS="525" /><SP WIDTH="4" VPOS="1239" HPOS="558" /><String WC="0.7680000067" CONTENT="27.12.2016" HEIGHT="13" WIDTH="86" VPOS="1239" HPOS="563" /></TextLine></TextBlock><TextBlock ID="Page1_Block65" HEIGHT="81" WIDTH="136" VPOS="1179" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="57" VPOS="1184" HPOS="855"><String WC="0.4480000138" CONTENT="15,00" HEIGHT="15" WIDTH="41" VPOS="1184" HPOS="855" /><SP WIDTH="4" VPOS="1184" HPOS="897" /><String WC="0.2199999988" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="1184" HPOS="902" /></TextLine></TextBlock><TextBlock ID="Page1_Block66" HEIGHT="81" WIDTH="169" VPOS="1179" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="57" VPOS="1184" HPOS="1021"><String WC="0.6259999871" CONTENT="15,00" HEIGHT="16" WIDTH="41" VPOS="1184" HPOS="1021" /><SP WIDTH="4" VPOS="1184" HPOS="1063" /><String WC="0.3400000036" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1184" HPOS="1068" /></TextLine></TextBlock><TextBlock ID="Page1_Block67" HEIGHT="54" WIDTH="46" VPOS="1260" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="5" VPOS="1268" HPOS="138"><String WC="0.8700000048" CONTENT="1" HEIGHT="13" WIDTH="5" VPOS="1268" HPOS="138" /></TextLine></TextBlock><TextBlock ID="Page1_Block68" HEIGHT="54" WIDTH="82" VPOS="1260" HPOS="169" language="de"><TextLine HEIGHT="15" WIDTH="32" VPOS="1267" HPOS="214"><String WC="0.6399999857" CONTENT="1,00" HEIGHT="15" WIDTH="32" VPOS="1267" HPOS="214" /></TextLine></TextBlock><TextBlock ID="Page1_Block69" HEIGHT="54" WIDTH="448" VPOS="1260" HPOS="333" language="de"><TextLine HEIGHT="18" WIDTH="203" VPOS="1266" HPOS="345"><String WC="0.8653846383" CONTENT="Blumengesteck" HEIGHT="17" WIDTH="118" VPOS="1267" HPOS="345" /><SP WIDTH="4" VPOS="1267" HPOS="464" /><String WC="0.6299999952" CONTENT="-" HEIGHT="2" WIDTH="5" VPOS="1274" HPOS="469" /><SP WIDTH="4" VPOS="1267" HPOS="475" /><String WC="0.8171428442" CONTENT="Empfang" HEIGHT="18" WIDTH="68" VPOS="1266" HPOS="480" /></TextLine><TextLine HEIGHT="15" WIDTH="425" VPOS="1294" HPOS="345"><String WC="0.5972727537" CONTENT="Gesamtsumme" HEIGHT="14" WIDTH="117" VPOS="1294" HPOS="345" /><SP WIDTH="4" VPOS="1294" HPOS="463" /><String WC="0.6299999952" CONTENT="des" HEIGHT="13" WIDTH="27" VPOS="1294" HPOS="468" /><SP WIDTH="5" VPOS="1294" HPOS="496" /><String WC="0.8108333349" CONTENT="Lieferschein" HEIGHT="13" WIDTH="92" VPOS="1294" HPOS="502" /><SP WIDTH="5" VPOS="1294" HPOS="595" /><String WC="0.8500000238" CONTENT="Nr." HEIGHT="13" WIDTH="21" VPOS="1294" HPOS="601" /><SP WIDTH="4" VPOS="1294" HPOS="623" /><String WC="0.7766666412" CONTENT="45034:" HEIGHT="13" WIDTH="52" VPOS="1294" HPOS="628" /><SP WIDTH="4" VPOS="1295" HPOS="681" /><String WC="0.5019999743" CONTENT="40,00" HEIGHT="15" WIDTH="43" VPOS="1294" HPOS="686" /><SP WIDTH="4" VPOS="1294" HPOS="730" /><String WC="1" CONTENT="EUR" HEIGHT="14" WIDTH="35" VPOS="1294" HPOS="735" /></TextLine></TextBlock><TextBlock ID="Page1_Block70" HEIGHT="54" WIDTH="136" VPOS="1260" HPOS="781" language="de"><TextLine HEIGHT="15" WIDTH="58" VPOS="1267" HPOS="854"><String WC="0.5460000038" CONTENT="40,00" HEIGHT="15" WIDTH="43" VPOS="1267" HPOS="854" /><SP WIDTH="3" VPOS="1267" HPOS="898" /><String WC="0.4300000072" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1267" HPOS="902" /></TextLine></TextBlock><TextBlock ID="Page1_Block71" HEIGHT="54" WIDTH="169" VPOS="1260" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="59" VPOS="1266" HPOS="1019"><String WC="0.6800000072" CONTENT="40,00" HEIGHT="16" WIDTH="44" VPOS="1266" HPOS="1019" /><SP WIDTH="3" VPOS="1266" HPOS="1064" /><String WC="0.2899999917" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="1266" HPOS="1068" /></TextLine></TextBlock><TextBlock ID="Page1_Block72" HEIGHT="29" WIDTH="210" VPOS="1314" HPOS="123" language="de"><TextLine HEIGHT="13" WIDTH="130" VPOS="1322" HPOS="137"><String WC="0.6953846216" CONTENT="Zwischensumme" HEIGHT="13" WIDTH="130" VPOS="1322" HPOS="137" /></TextLine></TextBlock><TextBlock ID="Page1_Block73" HEIGHT="29" WIDTH="169" VPOS="1314" HPOS="917" language="de"><TextLine HEIGHT="16" WIDTH="69" VPOS="1321" HPOS="1010"><String WC="0.9033333063" CONTENT="295,00" HEIGHT="15" WIDTH="54" VPOS="1322" HPOS="1010" /><SP WIDTH="3" VPOS="1321" HPOS="1065" /><String WC="0.4799999893" CONTENT="\xe2\x82\xac" HEIGHT="13" WIDTH="10" VPOS="1321" HPOS="1069" /></TextLine></TextBlock></ComposedBlock><ComposedBlock ID="Page2_Block9" HEIGHT="109" WIDTH="960" VPOS="865" HPOS="133" TYPE="table" xmlns="http://www.loc.gov/standards/alto/ns-v2#"><TextBlock ID="Page2_Block10" HEIGHT="30" WIDTH="794" VPOS="865" HPOS="133" language="de"><TextLine HEIGHT="14" WIDTH="106" VPOS="875" HPOS="144"><String WC="0.823333323" CONTENT="Gesamt" HEIGHT="14" WIDTH="60" VPOS="875" HPOS="144" /><SP WIDTH="4" VPOS="875" HPOS="205" /><String WC="0.59799999" CONTENT="Netto" HEIGHT="14" WIDTH="40" VPOS="875" HPOS="210" /></TextLine></TextBlock><TextBlock ID="Page2_Block11" HEIGHT="30" WIDTH="166" VPOS="865" HPOS="927" language="de"><TextLine HEIGHT="16" WIDTH="68" VPOS="873" HPOS="1017"><String WC="0.8500000238" CONTENT="295.00" HEIGHT="16" WIDTH="53" VPOS="873" HPOS="1017" /><SP WIDTH="3" VPOS="873" HPOS="1071" /><String WC="0.4799999893" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="873" HPOS="1075" /></TextLine></TextBlock><TextBlock ID="Page2_Block12" HEIGHT="27" WIDTH="794" VPOS="895" HPOS="133" language="de"><TextLine HEIGHT="19" WIDTH="776" VPOS="901" HPOS="144"><String WC="0.8799999952" CONTENT="zzgl." HEIGHT="16" WIDTH="34" VPOS="904" HPOS="144" /><SP WIDTH="5" VPOS="903" HPOS="179" /><String WC="0.7300000191" CONTENT="7,00" HEIGHT="16" WIDTH="33" VPOS="903" HPOS="185" /><SP WIDTH="3" VPOS="903" HPOS="219" /><String WC="1" CONTENT="%" HEIGHT="14" WIDTH="15" VPOS="903" HPOS="223" /><SP WIDTH="4" VPOS="903" HPOS="239" /><String WC="0.7774999738" CONTENT="USt." HEIGHT="14" WIDTH="32" VPOS="903" HPOS="244" /><SP WIDTH="4" VPOS="906" HPOS="277" /><String WC="0.8433333039" CONTENT="auf" HEIGHT="14" WIDTH="26" VPOS="903" HPOS="282" /><SP WIDTH="543" VPOS="902" HPOS="309" /><String WC="0.8683333397" CONTENT="295,00" HEIGHT="16" WIDTH="52" VPOS="901" HPOS="853" /><SP WIDTH="4" VPOS="901" HPOS="906" /><String WC="0.4900000095" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="9" VPOS="901" HPOS="911" /></TextLine></TextBlock><TextBlock ID="Page2_Block13" HEIGHT="27" WIDTH="166" VPOS="895" HPOS="927" language="de"><TextLine HEIGHT="16" WIDTH="58" VPOS="901" HPOS="1027"><String WC="0.773999989" CONTENT="20,65" HEIGHT="16" WIDTH="43" VPOS="901" HPOS="1027" /><SP WIDTH="3" VPOS="901" HPOS="1071" /><String WC="0.7699999809" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="10" VPOS="901" HPOS="1075" /></TextLine></TextBlock><TextBlock ID="Page2_Block14" HEIGHT="52" WIDTH="794" VPOS="922" HPOS="133" language="de"><TextLine HEIGHT="16" WIDTH="115" VPOS="952" HPOS="144"><String WC="0.5975000262" CONTENT="Gesamtbetrag" HEIGHT="16" WIDTH="115" VPOS="952" HPOS="144" /></TextLine></TextBlock><TextBlock ID="Page2_Block15" HEIGHT="52" WIDTH="166" VPOS="922" HPOS="927" language="de"><TextLine HEIGHT="16" WIDTH="67" VPOS="949" HPOS="1018"><String WC="0.6449999809" CONTENT="315,65" HEIGHT="16" WIDTH="53" VPOS="949" HPOS="1018" /><SP WIDTH="3" VPOS="949" HPOS="1072" /><String WC="0.3400000036" CONTENT="\xe2\x82\xac" HEIGHT="14" WIDTH="9" VPOS="949" HPOS="1076" /></TextLine></TextBlock></ComposedBlock>';

xml_data = ET.fromstring("<root>" + body+ "</root>")
data = xml_data.findall('ComposedBlock')
print(xml_data.tag)
print(xml_data.attrib)
for child_of_root in xml_data:
    rows = ''
    for text_block in child_of_root:
        columns = ''
        for text_line in text_block:
            column_data = ''
            for string_content in text_line:
                attribs = string_content.attrib
                if 'CONTENT' in attribs:
                    column_data = column_data  + string_content.attrib['CONTENT']

            columns = columns + column_data
        rows = rows + columns + ','
    rows = rows + '\n'

    print rows