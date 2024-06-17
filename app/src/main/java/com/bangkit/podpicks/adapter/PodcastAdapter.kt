package com.bangkit.podpicks.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bangkit.podpicks.R

class PodcastAdapter(private val data: List<String>) :
    RecyclerView.Adapter<PodcastAdapter.ChildViewHolder>() {

    class ChildViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val childTextView: TextView = itemView.findViewById(R.id.podcast_text)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChildViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_podcast, parent, false)
        return ChildViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChildViewHolder, position: Int) {
        holder.childTextView.text = data[position]
    }

    override fun getItemCount() = data.size
}