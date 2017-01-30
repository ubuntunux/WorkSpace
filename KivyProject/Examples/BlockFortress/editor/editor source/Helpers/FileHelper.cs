using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Windows.Forms;
using BlockFortressMapEditor.LevelModel;

namespace BlockFortressMapEditor.Helpers
{
    /// <summary>
    /// Helper class for managing files
    /// </summary>
    static class FileHelper
    {
        private const string fileExtension = ".lvl";
        private const string levelPath = "..\\levels";
        private const int maxAmountLevels = int.MaxValue;
        private const char emptyCharacter = '0';

        /// <summary>
        /// Deletes the specified file
        /// </summary>
        /// <param name="path">Path to file to delete</param>
        public static void DeleteLevel(string path)
        {
            File.Delete(path);
        }

        /// <summary>
        /// Returns all available levels
        /// </summary>
        /// <returns>List of level paths</returns>
        public static List<string> GetLevels()
        {
            string[] files = new string[0];
            try
            {
                files = Directory.GetFiles(levelPath);
            }
            catch (IOException e)
            {
                MessageBox.Show("Could not load level files. Is editor placed correctly?", "Level loading error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            List<string> levels = new List<string>();
            foreach (string s in files)
            {
                if (s.EndsWith(fileExtension))
                {
                    levels.Add(s);
                }
            }
            return levels;
        }

        /// <summary>
        /// Loads a level
        /// </summary>
        /// <param name="path">Path to level to load</param>
        /// <param name="width">Width of level</param>
        /// <param name="height">Height of level</param>
        /// <returns>The level loaded</returns>
        public static Level LoadLevel(string path, int width, int height)
        {
            Level level = new Level(width, height);
            string[] fileData = File.ReadAllText(path).Split(new string[]{" ", "\r\n", "\n"}, StringSplitOptions.RemoveEmptyEntries);
            int i = 0, j = 0;
            foreach (string s in fileData)
            {
                if (s.Equals("0"))
                {
                    level.SetData(i, j, null);
                }
                else
                {
                    bool visible = true;
                    string name = s;
                    if (name.StartsWith("-"))
                    {
                        visible = false;
                        name = name.Substring(1, s.Length - 1);
                    }
                    level.SetData(i, j, new LevelData(name, visible));
                }
                i++;
                if (i >= width)
                {
                    j++;
                    i = 0;
                    if (j >= height)
                    {
                        break;
                    }
                }
            }
            return level;
        }

        /// <summary>
        /// Creates a new level with the next available name
        /// <returns>Path to created file, or null if not created</returns>
        /// </summary>
        public static string NewLevel()
        {
            StringBuilder fileString = new StringBuilder();
            bool canCreate = false;
            for (int i = 1; i <= maxAmountLevels; i++)
            {
                fileString.Clear();
                fileString.Append(levelPath);
                fileString.Append("/");
                fileString.Append(i);
                fileString.Append(fileExtension);
                if (File.Exists(fileString.ToString()) == false)
                {
                    canCreate = true;
                    break;
                }
            }

            if (canCreate)
            {
                try
                {
                    File.Create(fileString.ToString()).Close();
                }
                catch (IOException exc)
                {
                    MessageBox.Show("Could not create new level: " + exc.Message, "Error!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return null;
                }
                return fileString.ToString();
            }
            else
            {
                MessageBox.Show("Could not create new level: No more room for levels", "Error!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return null;
            }
        }

        /// <summary>
        /// Saves the provided level to the specified path
        /// </summary>
        /// <param name="level">Level to save</param>
        /// <param name="path">Path to file</param>
        /// <returns>True if file was saved, otherwise false</returns>
        public static bool SaveLevel(Level level, string path)
        {
            StringBuilder stringBuilder = new StringBuilder();
            for (int i = 0; i < level.Height; i++)
            {
                for (int j = 0; j < level.Width; j++)
                {
                    LevelData data = level.GetData(j, i);
                    if (data != null)
                    {
                        if (data.Visible == false)
                        {
                            stringBuilder.Append("-");
                        }
                        stringBuilder.Append(data.Name);
                    }
                    else
                    {
                        stringBuilder.Append(emptyCharacter);
                    }
                    stringBuilder.Append(" ");
                }
                stringBuilder.Append("\r\n");
            }
            try
            {
                File.WriteAllText(path, stringBuilder.ToString());
            }
            catch (IOException e)
            {
                MessageBox.Show("Could not save level: " + e.Message, "Error!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }
            return true;
        }
    }
}
