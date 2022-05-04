# Bug fixed

https://user-images.githubusercontent.com/23220309/166812643-8b75ee4c-1886-4836-9a1a-899889a05f2b.mp4

Actually I just needed to call `self.update()` every time `y_values` changes.
Then
```kv
<Barchart>
  ...
  on_y_values: self.update()
```

Fixed it

