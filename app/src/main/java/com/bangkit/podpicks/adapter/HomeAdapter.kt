package com.bangkit.podpicks.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.bangkit.podpicks.R
import com.bangkit.podpicks.ui.home.HomeItem

class HomeAdapter(private val data: List<HomeItem>) :
    RecyclerView.Adapter<HomeAdapter.ParentViewHolder>() {

    class ParentViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val titleTextView: TextView = itemView.findViewById(R.id.home_title)
        val childRecyclerView: RecyclerView = itemView.findViewById(R.id.podcast_recycler_view)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ParentViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_home, parent, false)
        return ParentViewHolder(view)
    }

    override fun onBindViewHolder(holder: ParentViewHolder, position: Int) {
        val homeItem = data[position]
        holder.titleTextView.text = homeItem.title

        // Set up the inner RecyclerView
        holder.childRecyclerView.layoutManager = LinearLayoutManager(holder.itemView.context)
        holder.childRecyclerView.adapter = PodcastAdapter(homeItem.children)
    }

    override fun getItemCount() = data.size
}