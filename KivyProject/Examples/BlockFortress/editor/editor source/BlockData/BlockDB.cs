using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using System.IO;

namespace BlockFortressMapEditor.BlockData
{
    /// <summary>
    /// Database storing block images
    /// </summary>
    class BlockDB
    {
        /// <summary>
        /// The path used to find the block list metadata
        /// </summary>
        public string BlockListPath { get; private set; }
        
        private Dictionary<string, Image> blockDictionary = new Dictionary<string, Image>();

        /// <summary>
        /// Creates the BlockDB
        /// </summary>
        /// <param name="blockListPath">Path to block list metadata</param>
        public BlockDB(string blockListPath)
        {
            BlockListPath = blockListPath;
        }

        /// <summary>
        /// Loads blocks from the metadata specified in the block list file
        /// </summary>
        public void LoadBlocks()
        {
            string[] separators = new string[] { "=" };
            string[] data = File.ReadAllLines(BlockListPath);
            foreach (string s in data)
            {
                if (s.StartsWith("//") == false)
                {
                    string[] lineData = s.Split(separators, StringSplitOptions.RemoveEmptyEntries);
                    if (lineData.Length == 2)
                    {
                        string imageString = "../" + lineData[1].Substring(1, lineData[1].Length - 2);  // Strips them citations
                        try
                        {
                            Image image = Bitmap.FromFile(imageString);;
                            blockDictionary.Add(lineData[0], image);
                        }
                        catch (FileNotFoundException e)
                        {
                            // Image not found
                        }
                    }
                }
            }
        }

        /// <summary>
        /// Returns all available block names
        /// </summary>
        /// <returns>A list of strings containing block names</returns>
        public List<string> GetBlockNames()
        {
            return new List<string>(blockDictionary.Keys);
        }

        /// <summary>
        /// Returns the block image for a provided block name
        /// </summary>
        /// <param name="blockName">Name of the block</param>
        /// <returns>The block image</returns>
        public Image GetBlockImage(string blockName)
        {
            if (blockDictionary.ContainsKey(blockName))
            {
                return blockDictionary[blockName];
            }
            else
            {
                throw new ArgumentException("No such block exist!");
            }
        }

        /// <summary>
        /// Returns whether the given block is loaded
        /// </summary>
        /// <param name="blockName">Name of block</param>
        /// <returns>true if block is loaded, else false</returns>
        public bool HasBlock(string blockName)
        {
            return blockDictionary.ContainsKey(blockName);
        }
    }
}
