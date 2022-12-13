import datetime

from utils.procs.processor  import processor

class spareroom_create_proc(processor):

    def process(self, listing_dict, area):
        """Apply metadata attributes to the item

        Args:
            listing_dict (dict): Listing dictionary item to append attribute
            area (string): 'nearest' area where the listing was found
        """        
        d = listing_dict
        d['area'] = area
        d['area_codes']  = [area]
        d['created'] = str(datetime.datetime.now())
        d['updated'] = ''
        d['is_bold'] = "false"
        
        return d

class spareroom_update_proc(processor):
   
    def process(self, listing_dict, area):
        """_summary_

        Args:
            listing_dict (dict): Base document dictionary
            area (string): area to update

        Returns:
            _type_: _description_
        """    

        d = listing_dict
        d['updated'] = str(datetime.datetime.now())
        areas = d['area_codes']
        if areas is not None and not area in areas :
            d['area_codes']  = areas.append(area)
        elif areas is None:
            areas = [area]
        d['area_codes'] = areas

        return d
