using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using BlockFortressMapEditor.LevelModel;
using BlockFortressMapEditor.Helpers;
using BlockFortressMapEditor.BlockData;

namespace BlockFortressMapEditor
{
    public partial class MainForm : Form
    {
        private const string blockListPath = "..\\levels\\blocklist.txt";

        private const int blockWidth = 20;
        private const int blockHeight = 15;
        private const int levelWidth = 25;
        private const int levelHeight = 21;

        private Level currentLevel;
        private BlockDB blockDatabase;
        private string selectedItem;
        private int previousListBoxIndex = -1;
        private bool levelUnsaved;
        private bool renderBlockCursor;

        public MainForm()
        {
            InitializeComponent();
            SetLevelSelected(false);
            LoadLevelList();
            currentLevel = new Level(levelWidth, levelHeight);
            blockDatabase = new BlockDB(blockListPath);
            blockDatabase.LoadBlocks();
            InitializeBlockBrushes();
        }

        private void AboutClicked(object sender, EventArgs e)
        {
            MessageBox.Show("Level editor for Block Fortress"
                + "\r\nContributors: Robert Kaufmann",
                "About", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void BlockBrushClicked(object sender, EventArgs e)
        {
            Image img = null;
            selectedItem = sender.ToString();
            if (blockDatabase.HasBlock(selectedItem))
            {
                img = blockDatabase.GetBlockImage(selectedItem);
            }
            toolBrushButton.Image = img;
        }

        private void DeleteClicked(object sender, EventArgs e)
        {
            string path = (string)levelListBox.SelectedItem;
            DialogResult result = MessageBox.Show("Are you sure you wish to delete: " + path, "Are you sure?", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (result == System.Windows.Forms.DialogResult.Yes)
            {
                FileHelper.DeleteLevel(path);
                levelListBox.Items.Remove(path);
            }
        }

        private void ExitClicked(object sender, EventArgs e)
        {
            Close();
        }

        private void InitializeBlockBrushes()
        {
            EventHandler eventHandler = new EventHandler(BlockBrushClicked);
            var blockNames = blockDatabase.GetBlockNames();
            foreach (string s in blockNames)
            {
                toolBrushButton.DropDown.Items.Add(s, blockDatabase.GetBlockImage(s), eventHandler);
            }
            // Manually select the first brush
            if(toolBrushButton.DropDown.Items.Count > 0)
            {
                BlockBrushClicked(toolBrushButton.DropDown.Items[0], null);
            }
        }

        private void InstructionsClicked(object sender, EventArgs e)
        {
            MessageBox.Show("- Left mouse button to place block"
                + "\r\n- Right mouse button to remove block", "Instructions", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void InvisibleItemClicked(object sender, EventArgs e)
        {
            visibilityButton.Text = "Invisible";
        }

        private void LoadLevelList()
        {
            levelListBox.Items.Clear();
            foreach (string s in FileHelper.GetLevels())
            {
                levelListBox.Items.Add(s);
            }
        }

        private void LevelListSelectedIndexChanged(object sender, EventArgs e)
        {
            bool loadLevel = !levelUnsaved;
            if (previousListBoxIndex != -1 && levelListBox.SelectedIndex != previousListBoxIndex && levelUnsaved)
            {
                DialogResult result = MessageBox.Show("You are about to switch level. Do you want to save your current level?", "Question", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Question);
                if (result == System.Windows.Forms.DialogResult.Yes)
                {
                    loadLevel = true;
                    Save((string)levelListBox.Items[previousListBoxIndex]);
                }
                else if (result == System.Windows.Forms.DialogResult.Cancel)
                {
                    levelListBox.SelectedIndex = previousListBoxIndex;
                }
                else
                {
                    loadLevel = true;
                    SetLevelUnsaved(false);
                }
            }
            if (loadLevel && levelListBox.SelectedIndex != -1)
            {
                currentLevel = FileHelper.LoadLevel((string)levelListBox.SelectedItem, levelWidth, levelHeight);
                levelRenderBox.Refresh();
            }
            previousListBoxIndex = levelListBox.SelectedIndex;
            SetLevelSelected(levelListBox.SelectedItem != null);
        }

        private void LevelRenderBoxClicked(object sender, MouseEventArgs e)
        {
            Point location = e.Location;
            int posX = location.X / (blockWidth + 1);
            int posY = location.Y / (blockHeight + 1);
            if (e.Button == System.Windows.Forms.MouseButtons.Left)
            {
                bool visible = visibilityButton.Text.Equals("Visible");
                currentLevel.SetData(posX, posY, new LevelData(selectedItem, visible));
            }
            else
            {
                currentLevel.SetData(posX, posY, null);
            }
            SetLevelUnsaved(true);
            levelRenderBox.Refresh();
        }


        private void LevelRenderBoxMouseLeave(object sender, EventArgs e)
        {
            renderBlockCursor = false;
            levelRenderBox.Refresh();
        }

        private void LevelRenderBoxMouseMoved(object sender, MouseEventArgs e)
        {
            renderBlockCursor = true;
            levelRenderBox.Refresh();
        }

        private void NewClicked(object sender, EventArgs e)
        {
            string created = FileHelper.NewLevel();
            levelListBox.Items.Add(created);
        }

        private void PaintLevel(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            SolidBrush backgroundBrush = new SolidBrush(Color.LightGray);
            SolidBrush textBrush = new SolidBrush(Color.Black);
            // Draw level
            for (int i = 0; i < currentLevel.Width; i++)
            {
                for (int j = 0; j < currentLevel.Height; j++)
                {
                    Rectangle rect = new Rectangle(i * (blockWidth + 1), j * (blockHeight + 1),
                        blockWidth, blockHeight);
                    LevelData levelData = currentLevel.GetData(i, j);
                    if (levelData == null)
                    {
                        g.FillRectangle(backgroundBrush, rect);
                    }
                    else
                    {
                        Image image = blockDatabase.GetBlockImage(levelData.Name);
                        g.DrawImage(image, rect);
                        if (levelData.Visible == false)
                        {
                            g.DrawString("/////", Form.DefaultFont, textBrush, rect);
                        }
                    }
                }
            }
            // Draw selected block on level
            if (renderBlockCursor)
            {
                Point mousePos = levelRenderBox.PointToClient(Cursor.Position);
                int posX = mousePos.X / (blockWidth + 1);
                int posY = mousePos.Y / (blockHeight + 1);
                Rectangle mouseRect = new Rectangle(posX * (blockWidth + 1), posY * (blockHeight + 1), blockWidth, blockHeight);
                g.DrawImage(toolBrushButton.Image, mouseRect);
                if (visibilityButton.Text.Equals("Invisible"))
                {
                    g.DrawString("/////", Form.DefaultFont, textBrush, mouseRect);
                }
            }
        }

        private void SaveClicked(object sender, EventArgs e)
        {
            Save((string)levelListBox.SelectedItem);
        }

        private void Save(string path)
        {
            if (levelUnsaved)
            {
                if (FileHelper.SaveLevel(currentLevel, path))
                {
                    SetLevelUnsaved(false);
                }
            }
        }

        private void SetLevelSelected(bool selected)
        {
            saveButton.Enabled = selected;
            saveToolButton.Enabled = selected;
            saveMenuItem.Enabled = selected;
            deleteButton.Enabled = selected;
            deleteMenuItem.Enabled = selected;
            deleteToolButton.Enabled = selected;
            levelRenderBox.Visible = selected;
        }

        private void SetLevelUnsaved(bool unsaved)
        {
            if (levelUnsaved != unsaved)
            {
                levelUnsaved = unsaved;
                if (unsaved)
                {
                    Text += "*";
                    levelGroup.Text += "*";
                }
                else
                {
                    Text = Text.Substring(0, Text.Length - 1);
                    levelGroup.Text = levelGroup.Text.Substring(0, levelGroup.Text.Length - 1);
                }
            }
        }

        private void VisibleItemClicked(object sender, EventArgs e)
        {
            visibilityButton.Text = "Visible";
        }

        private void levelRenderBox_Click(object sender, EventArgs e)
        {

        }
    }
}
