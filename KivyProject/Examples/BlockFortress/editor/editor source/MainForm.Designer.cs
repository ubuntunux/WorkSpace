namespace BlockFortressMapEditor
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.saveButton = new System.Windows.Forms.Button();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.newToolButton = new System.Windows.Forms.ToolStripButton();
            this.saveToolButton = new System.Windows.Forms.ToolStripButton();
            this.deleteToolButton = new System.Windows.Forms.ToolStripButton();
            this.toolStripSeparator4 = new System.Windows.Forms.ToolStripSeparator();
            this.toolStripSeparator2 = new System.Windows.Forms.ToolStripSeparator();
            this.toolStripLabel2 = new System.Windows.Forms.ToolStripLabel();
            this.toolBrushButton = new System.Windows.Forms.ToolStripDropDownButton();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.visibilityButton = new System.Windows.Forms.ToolStripDropDownButton();
            this.visibleMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.invisibleMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.levelGroup = new System.Windows.Forms.GroupBox();
            this.levelRenderBox = new System.Windows.Forms.PictureBox();
            this.levelListBox = new System.Windows.Forms.ListBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.deleteButton = new System.Windows.Forms.Button();
            this.newButton = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.newToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.newMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.deleteMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.extrasToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.instructionsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStrip1.SuspendLayout();
            this.levelGroup.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.levelRenderBox)).BeginInit();
            this.groupBox2.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // saveButton
            // 
            this.saveButton.Image = global::BlockFortressMapEditor.Properties.Resources.saveFile;
            this.saveButton.ImageAlign = System.Drawing.ContentAlignment.TopCenter;
            this.saveButton.Location = new System.Drawing.Point(8, 332);
            this.saveButton.Name = "saveButton";
            this.saveButton.Size = new System.Drawing.Size(156, 23);
            this.saveButton.TabIndex = 0;
            this.saveButton.Text = "Save current";
            this.saveButton.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.saveButton.UseVisualStyleBackColor = true;
            this.saveButton.Click += new System.EventHandler(this.SaveClicked);
            // 
            // toolStrip1
            // 
            this.toolStrip1.BackColor = System.Drawing.SystemColors.Control;
            this.toolStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newToolButton,
            this.saveToolButton,
            this.deleteToolButton,
            this.toolStripSeparator4,
            this.toolStripSeparator2,
            this.toolStripLabel2,
            this.toolBrushButton,
            this.toolStripSeparator1,
            this.visibilityButton});
            this.toolStrip1.Location = new System.Drawing.Point(0, 24);
            this.toolStrip1.Name = "toolStrip1";
            this.toolStrip1.Size = new System.Drawing.Size(737, 25);
            this.toolStrip1.TabIndex = 2;
            this.toolStrip1.Text = "toolStrip1";
            // 
            // newToolButton
            // 
            this.newToolButton.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image;
            this.newToolButton.Image = global::BlockFortressMapEditor.Properties.Resources.newFile;
            this.newToolButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.newToolButton.Name = "newToolButton";
            this.newToolButton.Size = new System.Drawing.Size(23, 22);
            this.newToolButton.Text = "toolStripButton1";
            this.newToolButton.ToolTipText = "New level";
            this.newToolButton.Click += new System.EventHandler(this.NewClicked);
            // 
            // saveToolButton
            // 
            this.saveToolButton.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image;
            this.saveToolButton.Image = global::BlockFortressMapEditor.Properties.Resources.saveFile;
            this.saveToolButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.saveToolButton.Name = "saveToolButton";
            this.saveToolButton.Size = new System.Drawing.Size(23, 22);
            this.saveToolButton.Text = "toolStripButton2";
            this.saveToolButton.ToolTipText = "Save current level";
            this.saveToolButton.Click += new System.EventHandler(this.SaveClicked);
            // 
            // deleteToolButton
            // 
            this.deleteToolButton.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image;
            this.deleteToolButton.Image = global::BlockFortressMapEditor.Properties.Resources.deleteFile;
            this.deleteToolButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.deleteToolButton.Name = "deleteToolButton";
            this.deleteToolButton.Size = new System.Drawing.Size(23, 22);
            this.deleteToolButton.Text = "toolStripButton1";
            this.deleteToolButton.ToolTipText = "Delete current level";
            this.deleteToolButton.Click += new System.EventHandler(this.DeleteClicked);
            // 
            // toolStripSeparator4
            // 
            this.toolStripSeparator4.Name = "toolStripSeparator4";
            this.toolStripSeparator4.Size = new System.Drawing.Size(6, 25);
            // 
            // toolStripSeparator2
            // 
            this.toolStripSeparator2.Name = "toolStripSeparator2";
            this.toolStripSeparator2.Size = new System.Drawing.Size(6, 25);
            // 
            // toolStripLabel2
            // 
            this.toolStripLabel2.Name = "toolStripLabel2";
            this.toolStripLabel2.Size = new System.Drawing.Size(86, 22);
            this.toolStripLabel2.Text = "Selected block:";
            // 
            // toolBrushButton
            // 
            this.toolBrushButton.Image = ((System.Drawing.Image)(resources.GetObject("toolBrushButton.Image")));
            this.toolBrushButton.ImageScaling = System.Windows.Forms.ToolStripItemImageScaling.None;
            this.toolBrushButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolBrushButton.Name = "toolBrushButton";
            this.toolBrushButton.Size = new System.Drawing.Size(29, 22);
            this.toolBrushButton.TextImageRelation = System.Windows.Forms.TextImageRelation.TextBeforeImage;
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(6, 25);
            // 
            // visibilityButton
            // 
            this.visibilityButton.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.visibilityButton.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.visibleMenuItem,
            this.invisibleMenuItem});
            this.visibilityButton.Image = ((System.Drawing.Image)(resources.GetObject("visibilityButton.Image")));
            this.visibilityButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.visibilityButton.Name = "visibilityButton";
            this.visibilityButton.Size = new System.Drawing.Size(54, 22);
            this.visibilityButton.Text = "Visible";
            // 
            // visibleMenuItem
            // 
            this.visibleMenuItem.Name = "visibleMenuItem";
            this.visibleMenuItem.Size = new System.Drawing.Size(117, 22);
            this.visibleMenuItem.Text = "Visible";
            this.visibleMenuItem.Click += new System.EventHandler(this.VisibleItemClicked);
            // 
            // invisibleMenuItem
            // 
            this.invisibleMenuItem.Name = "invisibleMenuItem";
            this.invisibleMenuItem.Size = new System.Drawing.Size(117, 22);
            this.invisibleMenuItem.Text = "Invisible";
            this.invisibleMenuItem.Click += new System.EventHandler(this.InvisibleItemClicked);
            // 
            // levelGroup
            // 
            this.levelGroup.Controls.Add(this.levelRenderBox);
            this.levelGroup.Location = new System.Drawing.Point(12, 65);
            this.levelGroup.Name = "levelGroup";
            this.levelGroup.Size = new System.Drawing.Size(541, 366);
            this.levelGroup.TabIndex = 3;
            this.levelGroup.TabStop = false;
            this.levelGroup.Text = "Level workspace";
            // 
            // levelRenderBox
            // 
            this.levelRenderBox.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.levelRenderBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.levelRenderBox.Location = new System.Drawing.Point(6, 18);
            this.levelRenderBox.Name = "levelRenderBox";
            this.levelRenderBox.Size = new System.Drawing.Size(525, 337);
            this.levelRenderBox.TabIndex = 0;
            this.levelRenderBox.TabStop = false;
            this.levelRenderBox.Click += new System.EventHandler(this.levelRenderBox_Click);
            this.levelRenderBox.Paint += new System.Windows.Forms.PaintEventHandler(this.PaintLevel);
            this.levelRenderBox.MouseDown += new System.Windows.Forms.MouseEventHandler(this.LevelRenderBoxClicked);
            this.levelRenderBox.MouseLeave += new System.EventHandler(this.LevelRenderBoxMouseLeave);
            this.levelRenderBox.MouseMove += new System.Windows.Forms.MouseEventHandler(this.LevelRenderBoxMouseMoved);
            // 
            // levelListBox
            // 
            this.levelListBox.FormattingEnabled = true;
            this.levelListBox.Location = new System.Drawing.Point(6, 18);
            this.levelListBox.Name = "levelListBox";
            this.levelListBox.ScrollAlwaysVisible = true;
            this.levelListBox.Size = new System.Drawing.Size(156, 277);
            this.levelListBox.TabIndex = 4;
            this.levelListBox.SelectedIndexChanged += new System.EventHandler(this.LevelListSelectedIndexChanged);
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.deleteButton);
            this.groupBox2.Controls.Add(this.saveButton);
            this.groupBox2.Controls.Add(this.newButton);
            this.groupBox2.Controls.Add(this.levelListBox);
            this.groupBox2.Location = new System.Drawing.Point(555, 65);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(170, 366);
            this.groupBox2.TabIndex = 5;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Avaliable levels";
            // 
            // deleteButton
            // 
            this.deleteButton.Image = global::BlockFortressMapEditor.Properties.Resources.deleteFile;
            this.deleteButton.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.deleteButton.Location = new System.Drawing.Point(89, 303);
            this.deleteButton.Name = "deleteButton";
            this.deleteButton.Size = new System.Drawing.Size(75, 23);
            this.deleteButton.TabIndex = 6;
            this.deleteButton.Text = "Delete";
            this.deleteButton.UseVisualStyleBackColor = true;
            this.deleteButton.Click += new System.EventHandler(this.DeleteClicked);
            // 
            // newButton
            // 
            this.newButton.Image = global::BlockFortressMapEditor.Properties.Resources.newFile;
            this.newButton.Location = new System.Drawing.Point(8, 303);
            this.newButton.Name = "newButton";
            this.newButton.Size = new System.Drawing.Size(75, 23);
            this.newButton.TabIndex = 5;
            this.newButton.Text = "New";
            this.newButton.UseVisualStyleBackColor = true;
            this.newButton.Click += new System.EventHandler(this.NewClicked);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newToolStripMenuItem,
            this.extrasToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(737, 24);
            this.menuStrip1.TabIndex = 6;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // newToolStripMenuItem
            // 
            this.newToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newMenuItem,
            this.saveMenuItem,
            this.deleteMenuItem,
            this.exitMenuItem});
            this.newToolStripMenuItem.Name = "newToolStripMenuItem";
            this.newToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.newToolStripMenuItem.Text = "File";
            // 
            // newMenuItem
            // 
            this.newMenuItem.Image = global::BlockFortressMapEditor.Properties.Resources.newFile;
            this.newMenuItem.Name = "newMenuItem";
            this.newMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.N)));
            this.newMenuItem.Size = new System.Drawing.Size(176, 22);
            this.newMenuItem.Text = "New map";
            this.newMenuItem.Click += new System.EventHandler(this.NewClicked);
            // 
            // saveMenuItem
            // 
            this.saveMenuItem.Image = global::BlockFortressMapEditor.Properties.Resources.saveFile;
            this.saveMenuItem.Name = "saveMenuItem";
            this.saveMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.saveMenuItem.Size = new System.Drawing.Size(176, 22);
            this.saveMenuItem.Text = "Save map";
            this.saveMenuItem.Click += new System.EventHandler(this.SaveClicked);
            // 
            // deleteMenuItem
            // 
            this.deleteMenuItem.Image = global::BlockFortressMapEditor.Properties.Resources.deleteFile;
            this.deleteMenuItem.Name = "deleteMenuItem";
            this.deleteMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.D)));
            this.deleteMenuItem.Size = new System.Drawing.Size(176, 22);
            this.deleteMenuItem.Text = "Delete map";
            this.deleteMenuItem.Click += new System.EventHandler(this.DeleteClicked);
            // 
            // exitMenuItem
            // 
            this.exitMenuItem.Name = "exitMenuItem";
            this.exitMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Alt | System.Windows.Forms.Keys.F4)));
            this.exitMenuItem.Size = new System.Drawing.Size(176, 22);
            this.exitMenuItem.Text = "Exit";
            this.exitMenuItem.Click += new System.EventHandler(this.ExitClicked);
            // 
            // extrasToolStripMenuItem
            // 
            this.extrasToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.instructionsToolStripMenuItem,
            this.aboutToolStripMenuItem1});
            this.extrasToolStripMenuItem.Name = "extrasToolStripMenuItem";
            this.extrasToolStripMenuItem.Size = new System.Drawing.Size(44, 20);
            this.extrasToolStripMenuItem.Text = "Help";
            // 
            // instructionsToolStripMenuItem
            // 
            this.instructionsToolStripMenuItem.Name = "instructionsToolStripMenuItem";
            this.instructionsToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.F1;
            this.instructionsToolStripMenuItem.Size = new System.Drawing.Size(155, 22);
            this.instructionsToolStripMenuItem.Text = "Instructions";
            this.instructionsToolStripMenuItem.Click += new System.EventHandler(this.InstructionsClicked);
            // 
            // aboutToolStripMenuItem1
            // 
            this.aboutToolStripMenuItem1.Name = "aboutToolStripMenuItem1";
            this.aboutToolStripMenuItem1.Size = new System.Drawing.Size(155, 22);
            this.aboutToolStripMenuItem1.Text = "About";
            this.aboutToolStripMenuItem1.Click += new System.EventHandler(this.AboutClicked);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(737, 438);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.levelGroup);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(753, 476);
            this.Name = "MainForm";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.Text = "Block Fortress Level Editor";
            this.toolStrip1.ResumeLayout(false);
            this.toolStrip1.PerformLayout();
            this.levelGroup.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.levelRenderBox)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button saveButton;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.ToolStripButton newToolButton;
        private System.Windows.Forms.ToolStripButton saveToolButton;
        private System.Windows.Forms.GroupBox levelGroup;
        private System.Windows.Forms.ListBox levelListBox;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button newButton;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator4;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem newToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem newMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitMenuItem;
        private System.Windows.Forms.ToolStripMenuItem extrasToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem saveMenuItem;
        private System.Windows.Forms.PictureBox levelRenderBox;
        private System.Windows.Forms.ToolStripMenuItem instructionsToolStripMenuItem;
        private System.Windows.Forms.Button deleteButton;
        private System.Windows.Forms.ToolStripButton deleteToolButton;
        private System.Windows.Forms.ToolStripMenuItem deleteMenuItem;
        private System.Windows.Forms.ToolStripDropDownButton visibilityButton;
        private System.Windows.Forms.ToolStripMenuItem visibleMenuItem;
        private System.Windows.Forms.ToolStripMenuItem invisibleMenuItem;
        private System.Windows.Forms.ToolStripDropDownButton toolBrushButton;
        private System.Windows.Forms.ToolStripLabel toolStripLabel2;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator2;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
    }
}

