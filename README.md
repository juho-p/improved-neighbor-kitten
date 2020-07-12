# OBSOLETE

Kitty already handles this case when my PR was merged. This project is no longer.


# improved-neighbor-kitten
Kitten for improving the usage of Kitty-terminal splits layout. See https://github.com/kovidgoyal/kitty/

## Usage

Copy `improved_neighbors.py` to '~/.config/kitty`

Add key bindings. For example:

```
map kitty_mod+k kitten improved_neighbors.py activate top
map kitty_mod+h kitten improved_neighbors.py activate left
map kitty_mod+l kitten improved_neighbors.py activate right
map kitty_mod+j kitten improved_neighbors.py activate bottom

map ctrl+alt+shift+k kitten improved_neighbors.py move top
map ctrl+alt+shift+h kitten improved_neighbors.py move left
map ctrl+alt+shift+l kitten improved_neighbors.py move right
map ctrl+alt+shift+j kitten improved_neighbors.py move bottom
```

## License

Under GPL, just like Kitty is.
