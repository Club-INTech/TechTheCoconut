package
{
	import flash.desktop.Clipboard;
	import flash.display.MovieClip;
	import flash.display.Sprite;
	import flash.events.KeyboardEvent;
	import flash.events.MouseEvent;
	import flash.system.System;
	
	public class yeux_robot extends Sprite
	{
		public function yeux_robot()
		{	
			//Left eye
			for(var col:int=0; col<14 ; col++)
			{
				for(var row:int=0; row<7; row++)
				{
					var diode000:diode = new diode();
					diode000.name = "diode_"+row+"_"+col;
					diode000.x = 30*col +430;
					diode000.y = 30*row +270;
					addChild(diode000);
				}
			}
			//trace(diode(getChildByName("diode4")).value); //Code qui marche !
			
			stage.addEventListener(KeyboardEvent.KEY_DOWN, export);
		}
		public function export (e:KeyboardEvent)
		{
			var print:String = new String();
			switch(e.keyCode)
			{
				case 32 ://Touche espace -> print result
				print = "byte sprite[14]={";
				for(var col:int=0; col<14 ; col++)
				{
					print += "B";
					for(var row:int=0; row<7; row++)
					{
						print += diode(getChildByName("diode_"+row+"_"+col)).value;
					}
					if(col !=13)
						print += "0,"
				}
				//trace(diode(getChildByName("diode_3_1")).value);
				print +="0};";
				trace(print);
				System.setClipboard(print);
				break;
				
				case 46 : //Touche suppr -> Clear display
					for(col=0; col<14 ; col++)
					{
						for(row=0; row<7; row++)
						{
							
							diode(getChildByName("diode_"+row+"_"+col)).switchOFF();
						}
					}
					break;
				case 112: //Touche F1 -> Tout allumer
					for(col=0; col<14 ; col++)
					{
						for(row=0; row<7; row++)
						{
							
							diode(getChildByName("diode_"+row+"_"+col)).switchON();
						}
					}
					break;
			}
		}
	}
}