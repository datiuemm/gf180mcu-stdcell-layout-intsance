# Copyright 2026 Dat Dinh Trong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

import pya

class std_grid(pya.PCellDeclarationHelper):

    def __init__(self):
        super(std_grid, self).__init__()

        self.param("num_cols", self.TypeInt, "Number of Columns (Boxes)", default=3)
        self.param("num_rows", self.TypeInt, "Number of Rows (Boxes)", default=8)
        
        self.param("pitch_x", self.TypeDouble, "Pitch X", default=0.7, unit="um")
        self.param("pitch_y", self.TypeDouble, "Pitch Y", default=0.7, unit="um")
        
        self.param("offset_x", self.TypeDouble, "Offset X", default=0.0, unit="um")
        self.param("offset_y", self.TypeDouble, "Offset Y", default=0.35, unit="um")
        
        self.param("line_width", self.TypeDouble, "Line Width", default=0.0005, unit="um")

        self.param("layer_str", self.TypeString, "Grid Layer (Layer/Datatype)", default="0/0")

    def display_text_impl(self):
        return f"std_grid(Cols={self.num_cols}, Rows={self.num_rows})"

    def coerce_parameters_impl(self):
        if self.num_cols < 1: self.num_cols = 1
        if self.num_rows < 1: self.num_rows = 1
        if self.pitch_x <= 0: self.pitch_x = 0.1
        if self.pitch_y <= 0: self.pitch_y = 0.1

    def produce_impl(self):
        dbu = self.layout.dbu
        
        pitch_x_dbu = int(round(self.pitch_x / dbu))
        pitch_y_dbu = int(round(self.pitch_y / dbu))
        offset_x_dbu = int(round(self.offset_x / dbu))
        offset_y_dbu = int(round(self.offset_y / dbu))
        w_dbu = int(round(self.line_width / dbu))
        if w_dbu < 1: w_dbu = 1 

        try:
            layer_parts = self.layer_str.split("/")
            ln = int(layer_parts[0])
            ld = int(layer_parts[1]) if len(layer_parts) > 1 else 0
            target_layer = self.layout.layer(pya.LayerInfo(ln, ld))
        except:
            target_layer = self.layout.layer(pya.LayerInfo(0, 0))

        max_x = offset_x_dbu + self.num_cols * pitch_x_dbu
        max_y = offset_y_dbu + self.num_rows * pitch_y_dbu

        for c in range(self.num_cols + 1):
            x = offset_x_dbu + c * pitch_x_dbu
            box_v = pya.Box(x - w_dbu // 2, offset_y_dbu, x + w_dbu // 2, max_y)
            self.cell.shapes(target_layer).insert(box_v)

        for r in range(self.num_rows + 1):
            y = offset_y_dbu + r * pitch_y_dbu
            box_h = pya.Box(offset_x_dbu, y - w_dbu // 2, max_x, y + w_dbu // 2)
            self.cell.shapes(target_layer).insert(box_h)

        for c in range(self.num_cols):
            x1 = offset_x_dbu + c * pitch_x_dbu
            x2 = x1 + pitch_x_dbu
            
            for r in range(self.num_rows):
                y1 = offset_y_dbu + r * pitch_y_dbu
                y2 = y1 + pitch_y_dbu
                
                path1 = pya.Path([pya.Point(x1, y1), pya.Point(x2, y2)], w_dbu)
                self.cell.shapes(target_layer).insert(path1.simple_polygon())
                
                path2 = pya.Path([pya.Point(x1, y2), pya.Point(x2, y1)], w_dbu)
                self.cell.shapes(target_layer).insert(path2.simple_polygon())
