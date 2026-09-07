"""Bounded synthetic package smokes; run only in the selected isolated environment."""
import json,sys,pathlib,importlib.metadata,xml.etree.ElementTree as ET
from svg.path import parse_path
from svgelements import Path,Point,Matrix
import svgwrite

def main():
 versions={d.metadata['Name'].lower():d.version for d in importlib.metadata.distributions()}
 assert versions=={'svg.path':'7.1','svgelements':'1.9.6','svgwrite':'1.4.3'},versions
 a=parse_path('M0 0L3 4Z');assert len(a)==3 and a[1].end==3+4j
 b=Path('M0 0L3 4');assert b[-1].end==Point(3,4)
 transformed=Point(1,2)*Matrix('translate(2,3)');assert transformed==Point(3,5)
 drawing=svgwrite.Drawing(debug=True);drawing.add(drawing.line(start=(1,2),end=(3,4)));s=drawing.tostring();tree=ET.fromstring(s);line=tree.find('{http://www.w3.org/2000/svg}line');assert line is not None and line.attrib['x1']=='1' and line.attrib['y2']=='4'
 adverse={}
 for name,procedure in [('svg.path',lambda:parse_path('M 0')),('svgelements',lambda:Path('M 0')),('svgwrite',lambda:drawing.line(start=(0,0),end=(1,1),imaginary_attribute='x'))]:
  try:procedure()
  except (ValueError,TypeError,IndexError) as exc:adverse[name]={'refused':True,'error_type':type(exc).__name__}
  else:adverse[name]={'refused':False,'error_type':None}
 result={'schema':'ghc.family.svg-package-smokes.v1','versions':versions,'positive':{'svg.path':{'segments':3,'line_endpoint':[3,4],'closed_endpoint':[0,0]},'svgelements':{'line_endpoint':[3,4],'translated_point':[3,5]},'svgwrite':{'line_readback':{k:line.attrib[k] for k in ['x1','y1','x2','y2']},'xml_structure_preserved':True}},'adverse':adverse,'same_owner_only':True,'independent_reproduction':False,'shared_code_lineage':['svgelements acknowledges svg.path ancestry'],'host_environment_mutated':False,'real_drawings_or_rendering':0}
 pathlib.Path(sys.argv[1]).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(result));return 0 if all(x['refused'] for x in adverse.values()) else 2
if __name__=='__main__':raise SystemExit(main())
