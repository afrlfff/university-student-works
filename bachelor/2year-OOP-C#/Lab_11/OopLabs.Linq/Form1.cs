using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace OopLabs.Linq
{
    public partial class Form1 : Form
    {
        private ListBox ArtistsListBox;
        private ListBox AlbumsListBox;

        public Form1()
        {
            Text = "Albums";
            Size = new Size(300, 300);

            Label artistsLabel = new Label();
            artistsLabel.Text = "Исполнители";
            artistsLabel.Location = new Point(10, 10);
            Controls.Add(artistsLabel);

            ArtistsListBox = new ListBox();
            ArtistsListBox.Location = new Point(10, 30);
            ArtistsListBox.Size = new Size(200, 200);
            Controls.Add(ArtistsListBox);
            Load += Form1_Load;


            Label albumsLabel = new Label();
            albumsLabel.Text = "Альбомы";
            albumsLabel.Location = new Point(220, 10);
            Controls.Add(albumsLabel);

            AlbumsListBox = new ListBox();
            AlbumsListBox.Location = new Point(220, 30);
            AlbumsListBox.Size = new Size(200, 200);
            Controls.Add(AlbumsListBox);

            Load += Form1_Load;
            ArtistsListBox.SelectedIndexChanged += ArtistsListBox_SelectedIndexChanged;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            ArtistsListBox.DataSource = Album.GetAlbums()
                .OrderBy(x => x.Artist)
                .Select(album => album.Artist)
                .Distinct()
                .ToList();
        }
        private void ArtistsListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            string selectedArtist = (string)ArtistsListBox.SelectedItem;
            AlbumsListBox.DataSource = Album.GetAlbums()
                .Where(album => album.Artist == selectedArtist)
                .OrderByDescending(album => album.Date)
                .ToList();
        }
    }
}
